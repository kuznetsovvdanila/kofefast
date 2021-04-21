import functools
from io import BytesIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files import File
from django.shortcuts import render, redirect

from PIL import Image
import numpy as np
from geopy import Nominatim

from sklearn.cluster import KMeans

from kofe.additional_func import calculate_color, collect_items, collect_addresses, collect_relevant_coffeeshops
from kofe.decorators import add_user_buc, check_POST, check_proms
from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressUser, AddressCafe, ItemsSlotBasket, Basket, Item


@add_user_buc
@check_POST


def index_page(request):
    if request.method == 'POST':
        return redirect('index')
    drinkable, eatable = collect_items(request)
    addresses = collect_addresses(request)
    coffeeshops = Provider.objects.all()
    cafe_addresses = AddressCafe.objects.all()
    chosen_items = []

    flagCoffeeshops = False

    if request.user.is_authenticated:
        if request.user.chosen_address:
            flagCoffeeshops = True

    if flagCoffeeshops:
        adrs_user = request.user.chosen_address.all()
        coffeeshops, cafe_addresses = collect_relevant_coffeeshops(request, adrs_user)

    for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
        chosen_items.append(item)

    context = {
        'addresses': addresses if request.user.is_authenticated else None,
        'coffeeshops': coffeeshops if flagCoffeeshops else None,
        'providers': coffeeshops,
        'food': eatable,
        'drinks': drinkable,
        'form': RegistrationForm(),
        'chosen_items': chosen_items,
        'prvdr': chosen_items[0].good.provided if chosen_items else None,
        'basket': request.user.basket_set.all()[0],
        'chosen_address': request.user.chosen_address.all()[0] if request.user.chosen_address.all() else None,
    }
    return render(request, 'pages/index.html', context)


@check_proms
@check_POST
def personal_area_page(request):
    if request.method == 'POST':
        return redirect('personal_area')

    addresses = collect_addresses(request)

    context = {
        'addresses': addresses,
    }
    return render(request, 'pages/personal_area.html', context)


@add_user_buc
@check_proms
@check_POST
def basket_page(request):
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
