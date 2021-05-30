"""Написаны различные функции для view функций, с целью повышения читаемости оных"""
import re
import time
from io import BytesIO

from PIL import Image, ImageEnhance
from django.core.files import File
from geopy import Nominatim
from geopy import distance

from kofe.models import AddressUser, Provider, ItemsSlotBasket, AddressCafe, Order, Account


def remove_transparency(im, bg_colour=(255, 255, 255)):
    """Заменяет альфа канал на цвет(rgba->rgb)"""
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGB", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    return im


def collect_errors(request):
    """Проверка данных при регистрации на ошибки"""
    email = request.POST.get('email')
    phone_number = request.POST.get('phone_number')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # проверка пароля на сложность #
    res = [re.search(r"[a-z]", password1),
           re.search(r"[A-Z]", password1),
           re.search(r"[0-9]", password1),
           re.search(r"\W", password1)]

    email_exists = Account.objects.filter(email=email).exists()
    number_exists = Account.objects.filter(phone_number=phone_number).exists()
    dif_passwords = password1 != password2
    weak_password = not all(res)
    registration_error = any((email_exists, number_exists, dif_passwords, weak_password))

    return (email_exists, number_exists, dif_passwords, weak_password), registration_error


def collect_addresses(request):
    """Создание массива адресов пользователя"""
    addresses = []
    if request.user.is_authenticated:
        for adrs in AddressUser.objects.all().filter(owner=request.user):
            if request.user.chosen_address.all().filter(id=adrs.id):
                adrs.chosen = True
            addresses.append(adrs)
    return addresses


def collect_orders(request):
    """Создание массива заказов, совершенных пользователем"""
    orders = []
    if request.user.is_authenticated:
        for order in Order.objects.all().filter(customer=request.user):
            orders.append(order)
    return orders


def collect_relevant_coffeeshops(request, user_adrs):
    """Нахождение близких к пользователю кофеен"""
    coffeeshops = Provider.objects.all()
    cafe_addresses = AddressCafe.objects.all()
    geolocator = Nominatim(user_agent="kofefast")
    if user_adrs.all():
        coffeeshops = []
        cafe_addresses = []
        user_adrs = user_adrs.all()[0]
        try:
            user_location = geolocator.geocode(user_adrs)
        except:
            time.sleep(1)
            user_location = geolocator.geocode(user_adrs)
        if request.user.is_authenticated:
            if user_location:
                for adrs in AddressCafe.objects.all():
                    coffeeshop_address = str(adrs.city) + ', ' + str(adrs.street) + ', ' + \
                                         str(adrs.house)
                    try:
                        coffeeshop_location = geolocator.geocode(coffeeshop_address)
                    except:
                        time.sleep(1)
                        coffeeshop_location = geolocator.geocode(coffeeshop_address)
                    if distance.distance(
                            (user_location.longitude, user_location.latitude),
                            (coffeeshop_location.longitude, coffeeshop_location.latitude)).m < 1000:
                        coffeeshops.append(adrs.owner)
                        cafe_addresses.append(adrs)

                    print(distance.distance(
                        (user_location.longitude, user_location.latitude),
                        (coffeeshop_location.longitude, coffeeshop_location.latitude)))
            else:
                cafe_addresses = coffeeshops
    return coffeeshops, cafe_addresses


def collect_relevant_addresses(request, user_addresses, cafe_addresses, chosen_one):
    """Нахождение адресов пользоватея, находящихся в радиусе 1 км от адреса выбранной кофейни"""
    addresses = []
    if chosen_one:
        addresses.append(chosen_one)
    geolocator = Nominatim(user_agent="kofefast")
    for cafe_address in cafe_addresses:
        coffeeshop_address = str(cafe_address.city) + ', ' + str(cafe_address.street) + ', ' + \
                             str(cafe_address.house)
        try:
            coffeeshop_location = geolocator.geocode(coffeeshop_address)
        except:
            time.sleep(1)
            coffeeshop_location = geolocator.geocode(coffeeshop_address)
        for user_address in user_addresses:
            if chosen_one:
                if str(user_address.city) + str(user_address.street) + str(user_address.house) \
                        != str(chosen_one.city) + str(chosen_one.street) + str(chosen_one.house):
                    try:
                        user_location = geolocator.geocode(user_address)
                    except:
                        time.sleep(1)
                        user_location = geolocator.geocode(user_address)
                    if distance.distance(
                            (user_location.longitude, user_location.latitude),
                            (coffeeshop_location.longitude, coffeeshop_location.latitude)).m < 1000:
                        addresses.append(user_address)
            else:
                user_location = geolocator.geocode(user_address)
                if distance.distance(
                        (user_location.longitude, user_location.latitude),
                        (coffeeshop_location.longitude, coffeeshop_location.latitude)).m < 1000:
                    addresses.append(user_address)
    return addresses


def collect_items(request, chosen_items):
    """Создание массивов продуктов с дополнительными свойствами"""
    providers = Provider.objects.all()
    drinkable = []
    eatable = []

    def set_count(current_item):
        found = None
        if request.user.is_authenticated:
            found = ItemsSlotBasket.objects.all().\
                filter(good=current_item, basket_connection=request.user.basket_set.all()[0])
        if found:
            current_item.count = found[0].count
        else:
            current_item.count = 0

    for provider in providers:
        for item in provider.item_set.all():
            set_count(item)
            item.volumes = item.other_volumes.all()
            item.addons = item.additions.all()
            if item.not_has_color:
                calculate_color(item)
            if chosen_items:
                if item.provided == chosen_items[0].good.provided:
                    if item.type == 'd':
                        drinkable.append(item)
                    if item.type == 'e':
                        eatable.append(item)
            else:
                if item.type == 'd':
                    drinkable.append(item)
                if item.type == 'e':
                    eatable.append(item)

    return drinkable, eatable


def calculate_color(item):
    """Стилизация превью продукта"""
    img = Image.open(item.preview)
    if not img.mode == 'P':
        t = Image.open(item.preview)
        t = remove_transparency(t)
        t.convert('RGB')
        t = t.resize((int(800 * t.width / t.height), 800))
        t = ImageEnhance.Color(t).enhance(0.25)
        t_io = BytesIO()
        t.save(t_io, 'JPEG', quality=100)
        t_result = File(t_io, name=list(item.preview.name.split('/'))[1])
        item.preview = t_result

        item.not_has_color = False
        item.save()
