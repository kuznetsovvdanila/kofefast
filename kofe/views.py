"""Обработчики всех страниц сайта"""
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from kofe.additional_func import collect_items, collect_addresses, collect_relevant_coffeeshops, \
    collect_orders, collect_errors
from kofe.decorators import add_user_buc, check_POST, check_proms, check_admin_link, \
    synchronize_owned_owner
from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressCafe, ItemsSlotBasket


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
        return redirect('index')
    return {'email_exists': email_exists, 'number_exists': number_exists,
            'dif_passwords': dif_passwords, 'weak_password': weak_password}, registration_error


def login_user(request):
    """Авторизация пользователя"""

    account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
    if account:
        login(request, account)
    return True


@check_admin_link
@add_user_buc
@check_POST
def index_page(request):
    """View функция для index.html"""
    errors = {'email_exists': False, 'number_exists': False,
              'dif_passwords': False, 'weak_password': False}
    login_error = registration_error = False

    # регистрация и аутенфикация
    if request.method == 'POST':
        if request.POST.get('action_type') == 'authen':
            login_error = login_user(request)
        elif request.POST.get('action_type') == 'registr':
            errors, registration_error = registration_user(request)

    # инициализация переменных
    chosen_items = chosen_address_raw = coffeeshops = []
    flag_coffeeshops = flag_ca = False
    ca = None
    products = []

    if request.user.is_authenticated:
        # составление всех продуктов и предметов в корзине
        if ItemsSlotBasket.objects.all():
            for item in ItemsSlotBasket.objects.all().\
                    filter(basket_connection=request.user.basket_set.all()[0]):
                chosen_items.append(item)
        products = collect_items(request, chosen_items)

        # логика отображения кофейнь
        flag_coffeeshops = request.user.chosen_address
        if flag_coffeeshops:
            flag_ca = request.user.chosen_address.all()
            adrs_user = request.user.chosen_address.all()
            coffeeshops, _ = collect_relevant_coffeeshops(request, adrs_user)
        if flag_ca:
            chosen_address_raw = request.user.chosen_address.all()
            ca = request.user.chosen_address.all()[0]

    context = {
        'addresses': collect_addresses(request)
        if request.user.is_authenticated else None,
        'coffeeshops': Provider.objects.all()
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
    }
    return render(request, 'pages/index.html', context)


@check_proms
@synchronize_owned_owner
@check_POST
def personal_area_page(request):
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
        'production': production,
        'provider_addresses': provider_addresses,

        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('index')
