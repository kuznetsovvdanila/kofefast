from io import BytesIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files import File
from django.shortcuts import render, redirect

from PIL import Image
import numpy as np
from geopy import Nominatim

from sklearn.cluster import KMeans

from kofe.forms import RegistrationForm
from kofe.models import Provider, AddressUser


def index_page(request):
    form = None
    errors = None

    if request.method == 'POST':
        if request.POST.get('action_type') == 'authen':
            account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
            if account:
                login(request, account)
                return redirect('index')

        if request.POST.get('action_type') == 'registr':
            request.POST = request.POST.copy()
            request.POST['username'] = "lox"
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect('index')
            else:
                print(form.errors)

        if request.POST.get('action_type') == 'logout':
            return redirect('logout')

        if request.POST.get('action_type') == 'prefer_address':
            for i in request.user.chosen_address.all():
                request.user.chosen_address.remove(i)
            request.user.chosen_address.add(AddressUser.objects.all().filter(id=request.POST.get('prefered_adr_id'))[0])
            request.user.save()

        if request.POST.get('action_type') == 'delete_prefer_address':
            for i in request.user.chosen_address.all():
                request.user.chosen_address.remove(i)
            request.user.save()

    providers = Provider.objects.all()

    drinkable = []

    for provider in providers:
        for item in provider.item_set.all().filter(type='d'):
            if item.not_has_color:
                item.primary_color = ""
                img = Image.open(item.preview)
                if not img.mode == 'P':
                    img = img.resize((500, 500))

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
                    t = t.resize((int(500 * t.width / t.height), 500))
                    t_io = BytesIO()
                    t.save(t_io, 'JPEG')
                    t_result = File(t_io, name=item.preview.name)
                    item.preview = t_result

                    img = img.crop((0, 0, img.width / 2, img.height))

                    img = img.getdata()
                    img = np.array(img)

                    clt = KMeans(n_clusters=3)
                    clt.fit(img)

                    for cluster in enumerate(clt.cluster_centers_):
                        for color in cluster[1]:
                            item.primary_color += str(int(color)) + ", "
                        item.primary_color = item.primary_color[:-2]
                        item.not_has_color = False
                        item.save()
                        break

            drinkable.append(item)

    addresses = []
    if request.user.is_authenticated:
        for adrs in AddressUser.objects.all().filter(owner=request.user):
            if request.user.chosen_address.all().filter(id=adrs.id):
                adrs.chosen = True
            addresses.append(adrs)

    context = {
        # 'items': Provider.item_set.all().filter(type='d'),
        'addresses': addresses if request.user.is_authenticated else None,
        'providers': Provider.objects.all(),
        'drinks': drinkable,
        'form': form if form else RegistrationForm(),
        'errors': errors
    }
    #for provider in providers:
    #    print(provider.item_set.all().filter(type='d')[0])
    return render(request, 'pages/index.html', context)


def personal_area_page(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        if request.POST.get('action_type') == 'add_address':
            adr = AddressUser(owner=request.user, name=request.POST.get('name'), city=request.POST.get('city'), street=request.POST.get('street'),
                              house=request.POST.get('house'))
            if request.POST.get('entrance'):
                adr.entrance = request.POST.get('entrance')

            adr.save()
        if request.POST.get('action_type') == 'prefer_address':
            for i in request.user.chosen_address.all():
                request.user.chosen_address.remove(i)
            request.user.chosen_address.add(AddressUser.objects.all().filter(id=request.POST.get('prefered_adr_id'))[0])
            request.user.save()

        if request.POST.get('action_type') == 'delete_prefer_address':
            for i in request.user.chosen_address.all():
                request.user.chosen_address.remove(i)
            request.user.save()

        if request.POST.get('action_type') == 'changing_info':
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

        if request.POST.get('action_type') == 'delete_an_address':
            AddressUser.objects.all().filter(id=request.POST.get('delete_adr_id')).delete()

        return redirect('personal_area')

    addresses = []

    for adrs in AddressUser.objects.all().filter(owner=request.user):
        if request.user.chosen_address.all().filter(id=adrs.id):
            adrs.chosen = True
        addresses.append(adrs)

    context = {
        'addresses': addresses,
    }
    return render(request, 'pages/personal_area.html', context)


def basket_page(request):

    context = {

    }
    return render(request, 'pages/basket.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

