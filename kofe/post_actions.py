"""Функции, обрабатывающие все POST запросы"""
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.shortcuts import redirect
from environs import Env

from kofe.additional_func import collect_relevant_coffeeshops, remove_transparency
from kofe.models import AddressUser, ItemsSlotBasket, Item, Order, ItemsSlotOrder, AddressCafe


def logout_user(request):
    """Выход из аккаунта"""
    return redirect('logout')


def set_prefer_address(request):
    """Установка предпочтительного адреса"""
    request.user.y = 0
    request.user.save()
    if request.user.is_authenticated:
        for i in request.user.chosen_address.all():
            request.user.chosen_address.remove(i)
        if request.POST.get('prefered_adr_id'):
            if request.POST.get('prefered_adr_id') == 'addAnAddress':
                return redirect('personal_area')
            request.user.chosen_address.add(AddressUser.objects.all().
                                            filter(id=request.POST.get('prefered_adr_id'))[0])
            request.user.save()
    return redirect('index')


def change_basket(request, input_command):
    """Изменение содержания корзины"""
    if len(input_command) == 2:
        f = ItemsSlotBasket.objects.all().filter(good=Item.objects.all().
                                                 filter(id=int(input_command[1]))[0],
                                                 basket_connection=request.user.basket_set.all()[0])

        if request.POST.get('user_y'):
            request.user.y = int(request.POST.get('user_y'))
            request.user.save()
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
    """Очищение корзины"""
    request.user.y = 0
    request.user.save()
    ItemsSlotBasket.objects.all().delete()


def delete_prefer_address(request):
    """Удаление выбранного адреса"""
    request.user.y = 0
    request.user.save()
    for i in request.user.chosen_address.all():
        request.user.chosen_address.remove(i)
    request.user.save()


def add_address(request):
    """Добавление адреса в список адресов пользователя"""
    request.user.y = 0
    request.user.save()
    adr = AddressUser(owner=request.user, name=request.POST.get('name'),
                      city=request.POST.get('city'),
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
    """Изменение профиля пользователя"""
    request.user.y = 0
    request.user.save()

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
        request.user.profile_picture = request.FILES['profile_picture']
        t = Image.open(request.user.profile_picture)
        t = remove_transparency(t)
        t.convert('RGB')
        t_io = BytesIO()
        t.save(t_io, 'JPEG', quality=100)
        t_result = File(t_io, name=request.user.profile_picture.name)
        request.user.profile_picture = t_result
        request.user.save()


def delete_an_address(request):
    """Удаление предпочтительного адреса"""
    request.user.y = 0
    request.user.save()
    AddressUser.objects.all().filter(id=request.POST.get('delete_adr_id')).delete()


def make_an_order(request):
    """Создание заказа на index.html"""
    order = ''

    # Инициализация
    env = Env()
    env.read_env()
    sender = {'mail': env.str('sender_mail'),
              'password': env.str('password')}

    # Настройка протокола, по которому будет передаваться сообщение
    mailsender = smtplib.SMTP('smtp.gmail.com', 587)
    mailsender.starttls()
    mailsender.login(sender['mail'], sender['password'])

    # Информация о заказе
    msg = MIMEMultipart()
    msg['From'] = sender['mail']
    msg['To'] = str(request.user.email)
    msg.add_header('reply-to', sender['mail'])

    request.user.y = 0
    request.user.save()
    provider = request.user.basket_set.all()[0].chosen_items.all()[0].good.provided
    current_order = Order(customer=request.user,
                          comment=request.POST.get('comment'))

    _, cafe_addresses = collect_relevant_coffeeshops(request, request.user.chosen_address.all())

    for adrs in cafe_addresses:
        if adrs.owner == provider:
            current_order.chosen_cafe = adrs

    current_order.save()

    if request.user.chosen_address.all():
        current_order.chosen_delivery_address.add(request.user.chosen_address.all()[0])
    else:
        current_order.type_of_delivery = 'Самовывоз'

    current_order.save()

    for item in ItemsSlotBasket.objects.all().\
            filter(basket_connection=request.user.basket_set.all()[0]):
        i = ItemsSlotOrder(count=item.count, good=item.good, order_connection=current_order)
        i.save()
        order += str(i)
        order += ', '
        current_order.chosen_items.add(i)

    # отправка сообщения на почту
    mail_subject = f'Информация о заказе пользователя {request.user}'
    mail_body_text = 'Заказ: ' + order + f'Тип доставки: {current_order.type_of_delivery}; ' + \
                     f'Время оформления заказа: {current_order.time_created}; ' + \
                     f'Сообщение к заказу: {current_order.comment}'
    msg = MIMEText(mail_body_text, 'html', 'utf-8')
    msg['Subject'] = Header(mail_subject, 'utf-8')
    mailsender.sendmail(sender['mail'], str(request.user.email), msg.as_string())
    mailsender.quit()
    ##

    current_order.save()
    clear_the_basket(request)


def delete_item(request):
    """Удаление товара из продукции"""
    request.user.y = 0
    request.user.save()
    Item.objects.all().filter(id=request.POST.get('delete_item_id')).delete()


def change_item(request):
    """Изменение товара продукции"""
    request.user.y = 0
    request.user.save()

    if request.POST.get('itemId') == '0':
        current_item = Item(name=request.POST.get('item_name'),
                            description=request.POST.get('description'),
                            price=request.POST.get('item_price'),
                            provided=request.user.owned_cafe.all()[0],
                            type=request.POST.get('type'))
        current_item.preview = request.FILES['item_picture']
        t = Image.open(current_item.preview)
        t = remove_transparency(t)
        t.convert('RGB')
        t_io = BytesIO()
        t.save(t_io, 'JPEG', quality=100)
        t_result = File(t_io, name=request.user.profile_picture.name)
        current_item.preview = t_result
        current_item.save()

    else:
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
            t_io = BytesIO()
            t.save(t_io, 'JPEG', quality=100)
            t_result = File(t_io, name=request.user.profile_picture.name)
            item.preview = t_result
            item.save()


def add_address_provider(request):
    """Добавляет адрес"""
    request.user.y = 0
    request.user.save()
    current_address = AddressCafe(owner=request.user.owned_cafe.all()[0],
                                  city=request.POST.get('city'),
                                  street=request.POST.get('street'),
                                  house=request.POST.get('house'))

    if request.POST.get('building'):
        current_address.building = request.POST.get('building')

    if request.POST.get('entrance'):
        current_address.entrance = request.POST.get('entrance')

    current_address.save()


def delete_an_address_provider(request):
    """Удаляет адрес"""
    AddressCafe.objects.all().filter(id=request.POST.get('delete_adr_id')).delete()
