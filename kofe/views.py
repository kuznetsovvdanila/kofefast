import re

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from kofe.additional_func import collect_items, collect_addresses, collect_relevant_coffeeshops, \
    collect_orders, collect_relevant_addresses
from kofe.decorators import add_user_buc, check_POST, check_proms, check_admin_link, synchronize_owned_owner
from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressUser, AddressCafe, ItemsSlotBasket, Account

context = {}
registration_error = False
email_exists = False
number_exists = False
dif_passwords = False
weak_password = False

login_error = False


@check_admin_link
@add_user_buc
@check_POST
def index_page(request):
    global context, login_error, registration_error, email_exists, number_exists, dif_passwords, weak_password

    if request.method == 'POST':
        if request.POST.get('action_type') == 'registr':
            request.POST = request.POST.copy()
            form = RegistrationForm(request.POST)
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # проверка пароля на сложность #
            res = [re.search(r"[a-z]", password1), re.search(r"[A-Z]", password1), re.search(r"[0-9]", password1),
                   re.search(r"\W", password1)]

            if Account.objects.filter(email=email).exists():
                email_exists = True
                registration_error = True
            else:
                email_exists = False

            if Account.objects.filter(phone_number=phone_number).exists():
                number_exists = True
                registration_error = True
            else:
                number_exists = False

            if password1 != password2:
                dif_passwords = True
                registration_error = True
            else:
                dif_passwords = False

            if not all(res):
                weak_password = True
                registration_error = True
            else:
                weak_password = False

            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                phone_number = form.cleaned_data.get('phone_number')
                account = authenticate(email=email, password=raw_password, phone_number=phone_number)
                email_exists = False
                number_exists = False
                dif_passwords = False
                weak_password = False
                registration_error = False
                login_error = False
                login(request, account)
                return redirect('index')

        elif request.POST.get('action_type') == 'authen':
            account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
            login_error = True
            if account:
                login_error = False
                registration_error = False
                login(request, account)
            else:
                login_error = True

            return redirect('index')

    chosen_items = []
    addresses = collect_addresses(request)
    coffeeshops = Provider.objects.all()
    chosen_address_raw = []
    flag_coffeeshops = False
    flag_ca = False
    ca = None

    if request.user.is_authenticated:
        if ItemsSlotBasket.objects.all():
            for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
                chosen_items.append(item)
        drinkable, eatable = collect_items(request, chosen_items)

    if request.user.is_authenticated:
        if request.user.chosen_address:
            flag_coffeeshops = True

    if flag_coffeeshops:
        adrs_user = request.user.chosen_address.all()
        coffeeshops, cafe_addresses = collect_relevant_coffeeshops(request, adrs_user)

    if request.user.is_authenticated:
        if AddressUser.objects.all().filter(owner=request.user):
            if request.user.user_basket.all()[0].chosen_items.all():
                coffeeshop = request.user.user_basket.all()[0].chosen_items.all()[0].good.provided
                user_addresses = AddressUser.objects.all().filter(owner=request.user)
                chosen_one = request.user.chosen_address.all()[0] if request.user.chosen_address.all() else None
                addresses = collect_relevant_addresses(request,
                                                       user_addresses,
                                                       AddressCafe.objects.all().filter(owner=coffeeshop),
                                                       chosen_one)
        if request.user.chosen_address:
            if request.user.chosen_address.all():
                flag_ca = True
        if request.user.chosen_address.all():
            chosen_address_raw = request.user.chosen_address.all()

    if flag_ca:
        ca = request.user.chosen_address.all()[0]

    context = {
        'addresses': addresses if request.user.is_authenticated else None,
        'coffeeshops': coffeeshops if flag_coffeeshops else None,
        'providers': coffeeshops,
        'food': eatable if request.user.is_authenticated else None,
        'drinks': drinkable if request.user.is_authenticated else None,
        'form': RegistrationForm(),
        'chosen_items': chosen_items,
        'prvdr': chosen_items[0].good.provided if chosen_items else None,
        'basket': request.user.basket_set.all()[0] if request.user.is_authenticated and ItemsSlotBasket.objects.all() else None,
        'chosen_address_raw': chosen_address_raw,
        'chosen_address': ca if flag_ca else None,
        'email_exists': email_exists,
        'number_exists': number_exists,
        'dif_passwords': dif_passwords,
        'weak_password': weak_password,
        'registration_error': registration_error,
        'login_error': login_error
    }
    return render(request, 'pages/index.html', context)


@check_proms
@synchronize_owned_owner
@check_POST
def personal_area_page(request):
    global context
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
        'addresses': addresses,
        'orders': orders,
        'owned_cafe': request.user.owned_cafe.all()[0] if request.user.owned_cafe.all() else None,
        'production': production,
        'provider_addresses': provider_addresses,
    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')
