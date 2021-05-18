from io import BytesIO

import re
from random import choice

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from kofe.additional_func import collect_relevant_coffeeshops
from kofe.forms import RegistrationForm
from kofe.models import AddressUser, ItemsSlotBasket, Item, Account, Order, ItemsSlotOrder

from PIL import Image


def login_user(request):
    account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
    if account:
        login(request, account)


def registration_user(request):
    registration_error = email_exists = number_exists = dif_passwords = weak_password = False
    request.POST = request.POST.copy()
    form = RegistrationForm(request.POST)
    email = request.POST.get('email')
    phone_number = request.POST.get('phone_number')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # проверка пароля на сложность #
    res = [re.search(r"[a-z]", password1), re.search(r"[A-Z]", password1), re.search(r"[0-9]", password1), re.search(r"\W", password1)]

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



def logout_user(request):
    return redirect('logout')


def set_prefer_address(request):
    if request.user.is_authenticated:
        for i in request.user.chosen_address.all():
            request.user.chosen_address.remove(i)
        if request.POST.get('prefered_adr_id'):
            if request.POST.get('prefered_adr_id') == 'addAnAddress':
                return redirect('personal_area')
            else:
                request.user.chosen_address.add(AddressUser.objects.all().filter(id=request.POST.get('prefered_adr_id'))[0])
                request.user.save()


def change_basket(request, input_command):
    if len(input_command) == 2:
        f = ItemsSlotBasket.objects.all().filter(good=Item.objects.all().filter(id=int(input_command[1]))[0], basket_connection=request.user.basket_set.all()[0])
        if f:
            chosen_slot = f[0]
            if input_command[0] == 'add':
                chosen_slot.count += 1
            if input_command[0] == 'reduce':
                chosen_slot.count -= 1

            chosen_slot.save()
            if chosen_slot.count <= 0:
                chosen_slot.delete()
        else:
            if input_command[0] == 'add':
                te = ItemsSlotBasket(good=Item.objects.all().filter(id=int(input_command[1]))[0],
                                     count=1,
                                     basket_connection=request.user.basket_set.all()[0])
                te.save()
                request.user.basket_set.all()[0].chosen_items.add(te)
                request.user.save()


def clear_the_basket(request):
    ItemsSlotBasket.objects.all().delete()


def delete_prefer_address(request):
    for i in request.user.chosen_address.all():
        request.user.chosen_address.remove(i)
    request.user.save()


def add_address(request):
    adr = AddressUser(owner=request.user, name=request.POST.get('name'), city=request.POST.get('city'),
                      street=request.POST.get('street'),
                      house=request.POST.get('house'))
    if request.POST.get('entrance'):
        adr.entrance = request.POST.get('entrance')
    if request.POST.get('building'):
        adr.building = request.POST.get('building')
    if request.POST.get('floor'):
        adr.floor = request.POST.get('floor')
    if request.POST.get('flat'):
        adr.flat = request.POST.get('flat')

    adr.save()


def user_changing_info(request):
    def remove_transparency(im, bg_colour=(255, 255, 255)):
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            alpha = im.convert('RGBA').split()[-1]
            bg = Image.new("RGB", im.size, bg_colour + (255,))
            bg.paste(im, mask=alpha)
            return bg

        else:
            return im

    if request.POST.get('first_name'):
        first_name = request.POST.get('first_name')
        request.user.first_name = first_name
        request.user.save()

    if request.POST.get('last_name'):
        last_name = request.POST.get('last_name')
        request.user.last_name = last_name
        request.user.save()

    if request.POST.get('email'):
        email = request.POST.get('email')
        request.user.email = email
        request.user.save()

    if request.POST.get('phone_number'):
        phone_number = request.POST.get('phone_number')
        request.user.phone_number = phone_number
        request.user.save()

    if request.FILES:
        print('aeeee')
        request.user.profile_picture = request.FILES['profile_picture']
        t = Image.open(request.user.profile_picture)
        t = remove_transparency(t)
        t.convert('RGB')
        t.thumbnail((400, 400))
        t_io = BytesIO()
        t.save(t_io, 'JPEG')
        t_result = File(t_io, name=request.user.profile_picture.name)
        request.user.profile_picture = t_result
        request.user.save()


def delete_an_address(request):
    AddressUser.objects.all().filter(id=request.POST.get('delete_adr_id')).delete()


def make_an_order(request):
    user = request.user
    provider = user.basket_set.all()[0].chosen_items.all()[0].good.provided
    current_order = Order(customer=user,
                          comment=request.POST.get('comment'))

    adrs_user = request.user.chosen_address.all()
    coffeeshops, cafe_addresses = collect_relevant_coffeeshops(request, adrs_user)

    for adrs in cafe_addresses:
        if adrs.owner == provider:
            current_order.chosen_cafe = adrs

    if request.user.chosen_address.all():
        current_order.chosen_delivery_address.add(request.user.chosen_address.all()[0])
    else:
        current_order.type_of_delivery = 'Самовывоз'

    current_order.save()

    for item in ItemsSlotBasket.objects.all().filter(basket_connection=request.user.basket_set.all()[0]):
        i = ItemsSlotOrder(count=item.count, good=item.good, order_connection=current_order)
        i.save()
        current_order.chosen_items.add(i)
    current_order.save()
    clear_the_basket(request)


def delete_item(request):
    Item.objects.all().filter(id=request.POST.get('delete_item_id')).delete()


def change_item(request):
    def remove_transparency(im, bg_colour=(255, 255, 255)):
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            alpha = im.convert('RGBA').split()[-1]
            bg = Image.new("RGB", im.size, bg_colour + (255,))
            bg.paste(im, mask=alpha)
            return bg

        else:
            return im

    item = Item.objects.all().filter(id=request.POST.get('itemId'))[0]
    print(item)

    if request.POST.get('item_name'):
        item.name = request.POST.get('item_name')
        item.save()

    if request.POST.get('description'):
        item.description = request.POST.get('description')
        item.save()

    if request.POST.get('item_price'):
        item.price = request.POST.get('item_price')
        item.save()

    if request.FILES:
        item.preview = request.FILES['item_picture']
        t = Image.open(item.preview)
        t = remove_transparency(t)
        t.convert('RGB')
        t.thumbnail((400, 400))
        t_io = BytesIO()
        t.save(t_io, 'JPEG')
        t_result = File(t_io, name=request.user.profile_picture.name)
        item.preview = t_result
        item.save()
