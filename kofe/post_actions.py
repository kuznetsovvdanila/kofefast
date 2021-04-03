from io import BytesIO

from django.contrib.auth import login, authenticate
from django.core.files import File
from django.shortcuts import redirect

from kofe.forms import RegistrationForm
from kofe.models import AddressUser, ItemsSlotBasket, Item

from PIL import Image


def login_user(request):
    account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
    if account:
        login(request, account)


def registration_user(request):
    request.POST = request.POST.copy()
    request.POST['username'] = "lox"
    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        account = authenticate(email=email, password=raw_password)
        login(request, account)
    else:
        return redirect(form.errors, 'index')


def logout_user(request):
    return redirect('logout')


def set_prefer_address(request):
    print(request.POST)
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
        f = ItemsSlotBasket.objects.all().filter(good=Item.objects.all().filter(id=int(input_command[1]))[0])
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