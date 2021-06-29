"""Обработчики всех страниц сайта"""
import smtplib
import urllib.request
import urllib.parse
import random
from email.header import Header
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from environs import Env

from kofe.additional_func import collect_items, collect_addresses, collect_relevant_coffeeshops, \
    collect_orders, collect_errors, collect_relevant_addresses
from kofe.decorators import add_user_buc, check_POST, check_proms, check_admin_link, \
    synchronize_owned_owner
from kofe.forms import RegistrationForm
from kofe.models import AddressCafe, ItemsSlotBasket, AddressUser, Account

auth_open = False
password_change_error = False
password_change_final_error = False


def registration_user(request):
    """Регистрация пользователя"""

    request.POST = request.POST.copy()
    form = RegistrationForm(request.POST)

    (email_exists, number_exists, dif_passwords, weak_password), registration_error = \
        collect_errors(request)

    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        phone_number = form.cleaned_data.get('phone_number')
        account = authenticate(email=email, password=raw_password, phone_number=phone_number)
        login(request, account)
        return [redirect('index')]
    return [{'email_exists': email_exists, 'number_exists': number_exists,
            'dif_passwords': dif_passwords, 'weak_password': weak_password}, registration_error]


def login_user(request):
    """Авторизация пользователя"""

    account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
    if account:
        login(request, account)
    return True


def password_change(request):
    email = request.POST.get('email')
    if Account.objects.all().filter(email=email).exists():
        symbols = ['abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '0123456789']
        new_password = ''
        for i in range(8):
            rnd = random.randint(0, 2)
            if rnd == 0:
                new_password += symbols[0][random.randint(0, 25)]
            elif rnd == 1:
                new_password += symbols[1][random.randint(0, 25)]
            else:
                new_password += symbols[2][random.randint(0, 9)]

        url = "http://127.0.0.1:8000/"
        params = {
            'login': 'open',
            'password': new_password,
            'email': email,
        }
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        env = Env()
        env.read_env()
        sender = {'mail': env.str('sender_mail'),
                  'password': env.str('password')}

        message = 'Перейдите по ' \
                  '<a href="' + url + '">ссылке</a> для сброса старого пароля, ' \
                                      'после чего воспользуйтесь этим паролем: ' + new_password + \
                  ' для установки нового в личном кабинете. Если это были не вы, ' \
                  'просто проигнорируйте данное письмо.'

        msg = MIMEText(message, 'html', 'utf-8')

        msg['From'] = 'kofefast@internet.ru'
        msg['To'] = email
        msg['Subject'] = Header('Изменение пароля', 'utf-8')

        mailserver = smtplib.SMTP('smtp.mail.ru', 587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()

        mailserver.login(sender['mail'], sender['password'])

        mailserver.sendmail(msg['From'], msg['To'], msg.as_string())

        mailserver.quit()

    else:
        return True


def password_change_final(request):
    global password_change_final_error
    usr = request.user
    if usr.check_password(request.POST.get('password_old')) and \
            request.POST.get('password1') == request.POST.get('password2'):
        usr.set_password(request.POST.get('password1'))
        usr.save()
        login(request, usr)
        return True
    else:
        password_change_final_error = True
        return False


@check_admin_link
@add_user_buc
@check_POST
def index_page(request):
    """View функция для index.html"""
    global auth_open, password_change_error, password_change_final_error
    password_change_final_error = False
    if request.GET and not request.user.is_authenticated:
        if request.GET['login']:
            auth_open = True
        if request.GET['password'] and request.GET['email']:
            usr = Account.objects.all().filter(email=request.GET['email'])[0]
            usr.set_password(request.GET['password'])
            usr.save()
            login(request, usr)
            return redirect('index')

    errors = {'email_exists': False, 'number_exists': False,
              'dif_passwords': False, 'weak_password': False}
    login_error = registration_error = False

    # регистрация и аутентификация
    if request.method == 'POST':
        if request.POST.get('action_type') == 'authen':
            auth_open = password_change_error = False
            login_error = login_user(request)
        elif request.POST.get('action_type') == 'registr':
            t = registration_user(request)
            if len(t) == 1:
                auth_open = password_change_error = False
                return t[0]
            else:
                errors = t[0]
                auth_open = password_change_error = False
                registration_error = t[1]
        elif request.POST.get('action_type') == 'password_change':
            auth_open = password_change_error = password_change(request)

    # инициализация переменных
    chosen_items = chosen_address_raw = coffeeshops = []
    flag_coffeeshops = flag_ca = False
    ca = None
    products = []
    cafe_addresses = []
    addresses = collect_addresses(request)
    if request.user.is_authenticated:
        # составление всех продуктов и предметов в корзине
        if AddressUser.objects.all().filter(owner=request.user):
            if request.user.user_basket.all()[0].chosen_items.all():
                coffeeshop = request.user.user_basket.all()[0].chosen_items.all()[0].good.provided
                user_addresses = AddressUser.objects.all().filter(owner=request.user)
                chosen_one = request.user.chosen_address.all()[0] if request.user.chosen_address.all() else None
                addresses = collect_relevant_addresses(request, user_addresses, coffeeshop,
                                                       AddressCafe.objects.all().filter(owner=coffeeshop), chosen_one)
                if not request.user.chosen_address.all():
                    cafe_addresses = AddressCafe.objects.all().filter(owner=coffeeshop)

        if ItemsSlotBasket.objects.all():
            for item in ItemsSlotBasket.objects.all().\
                    filter(basket_connection=request.user.basket_set.all()[0]):
                chosen_items.append(item)
        products = collect_items(request, chosen_items)

        # логика отображения кофеен
        flag_coffeeshops = request.user.chosen_address
        if flag_coffeeshops:
            flag_ca = request.user.chosen_address.all()
            adrs_user = request.user.chosen_address.all()
            coffeeshops, _ = collect_relevant_coffeeshops(request, adrs_user)
        if flag_ca:
            chosen_address_raw = request.user.chosen_address.all()
            ca = request.user.chosen_address.all()[0]

    context = {
        'addresses': addresses
        if request.user.is_authenticated else None,
        'coffeeshops': coffeeshops
        if flag_coffeeshops else None,
        'food': products[1]
        if request.user.is_authenticated else None,
        'drinks': products[0]
        if request.user.is_authenticated else None,
        'prvdr': chosen_items[0].good.provided
        if chosen_items else None,
        'basket': request.user.basket_set.all()[0]
        if request.user.is_authenticated and ItemsSlotBasket.objects.all() else None,
        'chosen_address': ca
        if flag_ca else None,
        'email_exists': errors['email_exists'],
        'number_exists': errors['number_exists'],
        'dif_passwords': errors['dif_passwords'],
        'weak_password': errors['weak_password'],
        'registration_error': registration_error,
        'login_error': login_error,
        'providers': coffeeshops,
        'chosen_items': chosen_items,
        'chosen_address_raw': chosen_address_raw,
        'form': RegistrationForm(),
        'auth_open': auth_open,
        'password_change_error': password_change_error,
        'cafe_addresses': cafe_addresses,
    }
    return render(request, 'pages/index.html', context)


@check_proms
@synchronize_owned_owner
@check_POST
def personal_area_page(request):
    global password_change_final_error
    password_change_final_error = False
    """View функция для страницы пользователя"""
    if request.method == 'POST':
        return redirect('personal_area')

    orders = collect_orders(request)
    addresses = collect_addresses(request)

    production = []
    provider_addresses = []

    if request.user.is_cafe_owner:
        if request.user.owned_cafe.all():
            production = request.user.owned_cafe.all()[0].item_set.all()
        if AddressCafe.objects.all():
            for address in AddressCafe.objects.all():
                if address.owner == request.user.owned_cafe.all()[0]:
                    provider_addresses.append(address)

    context = {
        'owned_cafe': request.user.owned_cafe.all()[0]
        if request.user.owned_cafe.all() else None,
        'production': production[::-1],
        'provider_addresses': provider_addresses[::-1],
        'addresses': addresses[::-1],
        'orders': orders[::-1],
    }
    return render(request, 'pages/personal_area.html', context)


@check_proms
@check_POST
def change_password(request):
    context = {
        'email': request.user.email,
        'password_change_final_error': password_change_final_error,
    }
    if request.method == 'POST':
        if password_change_final(request):
            return redirect('personal_area')
        else:
            return render(request, 'pages/change_password.html', context)
    return render(request, 'pages/change_password.html', context)


def logoutUser(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('index')
