import functools
import re
from io import BytesIO

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files import File
from django.shortcuts import render, redirect

from PIL import Image
import numpy as np
from geopy import Nominatim

from kofe.additional_func import calculate_color, collect_items, collect_addresses, collect_relevant_coffeeshops, \
    collect_orders
from kofe.decorators import add_user_buc, check_POST, check_proms, check_admin_link
from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressUser, AddressCafe, ItemsSlotBasket, Basket, Item, Account

context = {}


@check_admin_link
@add_user_buc
@check_POST
def index_page(request):
    global context
    registration_error = email_exists = number_exists = dif_passwords = weak_password = False

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
            if Account.objects.filter(phone_number=phone_number).exists():
                number_exists = True
            if password1 != password2:
                dif_passwords = True
            if not all(res):
                weak_password = True

            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                phone_number = form.cleaned_data.get('phone_number')
                account = authenticate(email=email, password=raw_password, phone_number=phone_number)
                login(request, account)
                return redirect('index')
        else:
            return redirect('index')

    if request.user.is_authenticated:
        drinkable, eatable = collect_items(request)
    addresses = collect_addresses(request)
    coffeeshops = Provider.objects.all()
    cafe_addresses = AddressCafe.objects.all()
    chosen_items = []
    CA = None

    flagCoffeeshops = False
    flagCA = False

    if request.user.is_authenticated:
        if request.user.chosen_address:
            flagCoffeeshops = True

    if flagCoffeeshops:
        adrs_user = request.user.chosen_address.all()
        coffeeshops, cafe_addresses = collect_relevant_coffeeshops(request, adrs_user)

    if request.user.is_authenticated:
        if request.user.chosen_address.all():
            flagCA = True
        for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
            chosen_items.append(item)

    if flagCA:
        CA = request.user.chosen_address.all()[0]

    context = {
        'addresses': addresses if request.user.is_authenticated else None,
        'coffeeshops': coffeeshops if flagCoffeeshops else None,
        'providers': coffeeshops,
        'food': eatable if request.user.is_authenticated else None,
        'drinks': drinkable if request.user.is_authenticated else None,
        'form': RegistrationForm(),
        'chosen_items': chosen_items,
        'prvdr': chosen_items[0].good.provided if chosen_items else None,
        'basket': request.user.basket_set.all()[0] if request.user.is_authenticated else None,
        'chosen_address': CA if flagCA else None,
        'errors': [email_exists, number_exists, dif_passwords, weak_password],
    }
    print(context)
    return render(request, 'pages/index.html', context)


@check_proms
@check_POST
def personal_area_page(request):
    global context
    if request.method == 'POST':
        return redirect('personal_area')

    orders = collect_orders(request)
    addresses = collect_addresses(request)

    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'pages/personal_area.html', context)


@add_user_buc
@check_proms
@check_POST
def basket_page(request):
    global context
    if request.method == 'POST':
        return redirect('basket')

    basket = request.user.basket_set.all()[0]
    chosen_items = []
    for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
        chosen_items.append(item)

    context = {
        'cafe_addresses': AddressCafe.objects.all(),
        'provider': chosen_items[0].good.provided if chosen_items else None,
        'chosen_items': chosen_items,
        'basket': basket,
    }
    return render(request, 'pages/basket.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')
