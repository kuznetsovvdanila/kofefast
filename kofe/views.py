from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from kofe.additional_func import collect_items, collect_addresses, collect_relevant_coffeeshops, \
    collect_orders, collect_relevant_addresses, collect_errors
from kofe.decorators import add_user_buc, check_POST, check_proms, check_admin_link, synchronize_owned_owner
from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressUser, AddressCafe, ItemsSlotBasket, Account

context = {}
login_error = email_exists = number_exists = dif_passwords = weak_password = registration_error = False


def registration_user(request):
    global email_exists, number_exists, dif_passwords, weak_password, registration_error

    request.POST = request.POST.copy()
    form = RegistrationForm(request.POST)

    (email_exists, number_exists, dif_passwords, weak_password), registration_error = \
        collect_errors(request, {'email_exists': email_exists,
                             'number_exists': number_exists,
                             'dif_passwords': dif_passwords,
                             'weak_password': weak_password,
                             'registration_error': registration_error}, registration_error)

    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        phone_number = form.cleaned_data.get('phone_number')
        account = authenticate(email=email, password=raw_password, phone_number=phone_number)
        login(request, account)
        return redirect('index')


def login_user(request):
    global login_error

    account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
    login_error = True
    if account:
        login(request, account)


@check_admin_link
@add_user_buc
@check_POST
def index_page(request):
    global context
    global email_exists, number_exists, dif_passwords, weak_password, registration_error

    # регистрация и аутенфикация
    post_actions = {'authen': login_user, 'registr': registration_user}
    if request.method == 'POST':
        if request.POST.get('action_type') in post_actions:
            t = post_actions[request.POST.get('action_type')](request)
            if t:
                return t

    # инициализация переменных
    chosen_items = chosen_address_raw = drinkable = eatable = []
    flag_coffeeshops = flag_ca = False
    ca = None
    addresses = collect_addresses(request)
    coffeeshops = Provider.objects.all()

    if request.user.is_authenticated:
        # составление всех продуктов и предметов в корзине
        if ItemsSlotBasket.objects.all():
            for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
                chosen_items.append(item)
        drinkable, eatable = collect_items(request, chosen_items)

        # подгон сайта под владельцев кофейнь
        if AddressUser.objects.all().filter(owner=request.user):
            if request.user.user_basket.all()[0].chosen_items.all():
                coffeeshop = request.user.user_basket.all()[0].chosen_items.all()[0].good.provided
                user_addresses = AddressUser.objects.all().filter(owner=request.user)
                chosen_one = request.user.chosen_address.all()[0] if request.user.chosen_address.all() else None
                addresses = collect_relevant_addresses(request,
                                                       user_addresses,
                                                       AddressCafe.objects.all().filter(owner=coffeeshop),
                                                       chosen_one)
        # логика отображения кофейнь
        flag_coffeeshops = request.user.chosen_address
        if flag_coffeeshops:
            flag_ca = request.user.chosen_address.all()
            adrs_user = request.user.chosen_address.all()
            coffeeshops, cafe_addresses = collect_relevant_coffeeshops(request, adrs_user)
        if flag_ca:
            chosen_address_raw = request.user.chosen_address.all()
            ca = request.user.chosen_address.all()[0]

    context = {
        'addresses': addresses
        if request.user.is_authenticated else None,
        'coffeeshops': coffeeshops
        if flag_coffeeshops else None,
        'food': eatable
        if request.user.is_authenticated else None,
        'drinks': drinkable
        if request.user.is_authenticated else None,
        'prvdr': chosen_items[0].good.provided
        if chosen_items else None,
        'basket': request.user.basket_set.all()[0]
        if request.user.is_authenticated and ItemsSlotBasket.objects.all() else None,
        'chosen_address': ca
        if flag_ca else None,
        'email_exists': email_exists,
        'number_exists': number_exists,
        'dif_passwords': dif_passwords,
        'weak_password': weak_password,
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
        'owned_cafe': request.user.owned_cafe.all()[0]
        if request.user.owned_cafe.all() else None,
        'production': production,
        'provider_addresses': provider_addresses,

        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')
