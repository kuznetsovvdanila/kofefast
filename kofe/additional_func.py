from io import BytesIO
from math import sqrt

import numpy as np
from PIL import Image, ImageEnhance
from django.core.files import File

from kofe.models import AddressUser, Provider, ItemsSlotBasket, AddressCafe

from geopy import Nominatim
from geopy import distance


def collect_addresses(request):
    addresses = []
    if request.user.is_authenticated:
        for adrs in AddressUser.objects.all().filter(owner=request.user):
            if request.user.chosen_address.all().filter(id=adrs.id):
                adrs.chosen = True
            addresses.append(adrs)
    return addresses


def collect_relevant_coffeeshops(request, user_adrs):
    coffeeshops = Provider.objects.all()
    cafe_addresses = AddressCafe.objects.all()
    geolocator = Nominatim(user_agent="kofefast")
    if user_adrs.all():
        coffeeshops = []
        cafe_addresses = []
        user_adrs = user_adrs.all()[0]
        user_location = geolocator.geocode(user_adrs)
        if request.user.is_authenticated:
            for adrs in AddressCafe.objects.all():
                coffeeshop_address = str(adrs.city) + ', ' + str(adrs.street) + ', ' + str(adrs.house)
                coffeeshop_location = geolocator.geocode(coffeeshop_address)
                if distance.distance((user_location.longitude, user_location.latitude), (coffeeshop_location.longitude, coffeeshop_location.latitude)).m < 1000:
                    coffeeshops.append(adrs.owner)
                    cafe_addresses.append(adrs)
    return coffeeshops, cafe_addresses


def collect_items(request):
    providers = Provider.objects.all()
    drinkable = []
    eatable = []

    def set_count(current_item):
        found = ItemsSlotBasket.objects.all().filter(good=current_item, basket_connection=request.user.basket_set.all()[0])
        if found:
            current_item.count = found[0].count
        else:
            current_item.count = 0

    for provider in providers:
        for item in provider.item_set.all():
            set_count(item)
            if item.not_has_color:
                calculate_color(item)
            if item.type == 'd':
                drinkable.append(item)
            if item.type == 'e':
                eatable.append(item)

    return drinkable, eatable


def calculate_color(item):
    img = Image.open(item.preview)
    if not img.mode == 'P':

        def remove_transparency(im, bg_colour=(255, 255, 255)):
            if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                alpha = im.convert('RGBA').split()[-1]
                bg = Image.new("RGB", im.size, bg_colour + (255,))
                bg.paste(im, mask=alpha)
                return bg

            else:
                return im

        t = Image.open(item.preview)
        t = remove_transparency(t)
        t.convert('RGB')
        t = t.resize((int(800 * t.width / t.height), 800))
        t = ImageEnhance.Color(t).enhance(0.15)
        t_io = BytesIO()
        t.save(t_io, 'JPEG')
        t_result = File(t_io, name=list(item.preview.name.split('/'))[1])
        item.preview = t_result

        item.not_has_color = False
        item.save()
