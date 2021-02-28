from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from PIL import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from kofe.models import Provider, Address


def index_page(request):
    form = None
    errors = None

    if request.method == 'POST':
        if request.POST.get('action_type') == 'authen':
            password = request.POST.get('password1')
            t = User.objects.all().filter(email=request.POST.get('email'))
            if t:
                username = t[0]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    print('ne')
                    errors = True
            else:
                print('nene')

        if request.POST.get('action_type') == 'registr':
            request.POST = request.POST.copy()
            t = list(map(str, request.POST.get('email').split('@')))
            request.POST['username'] = t[0] + t[1]
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.email = request.POST.get('email')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.save()
                login(request, user)
                return redirect('index')
            else:
                print(form.errors)

        if request.POST.get('action_type') == 'logout':
            return redirect('logout')

    providers = Provider.objects.all()

    drinkable = []

    for provider in providers:
        for item in provider.item_set.all().filter(type='d'):
            if item.not_has_color:
                item.primary_color = ""
                img = Image.open(item.preview)
                img = img.resize((200, 200))

                def remove_transparency(im, bg_colour=(255, 255, 255)):

                    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
                    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

                        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
                        alpha = im.convert('RGBA').split()[-1]

                        # Create a new background image of our matt color.
                        # Must be RGBA because paste requires both images have the same format
                        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
                        bg = Image.new("RGBA", im.size, bg_colour + (255,))
                        bg.paste(im, mask=alpha)
                        return bg

                    else:
                        return im

                img = remove_transparency(img)
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

    context = {
        # 'items': Provider.item_set.all().filter(type='d'),
        'providers': Provider.objects.all(),
        'drinks': drinkable,
        'form': form if form else UserCreationForm(),
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
            adr = Address(owner=request.user,
                          city=request.POST.get('city'),
                          street=request.POST.get('street'),
                          house=int(request.POST.get('house')))
            if request.POST.get('entrance'):
                adr.entrance = request.POST.get('entrance')

            adr.save()

    addresses = []

    for adrs in Address.objects.all().filter(owner=request.user):
        addresses.append(adrs)

    context = {
        'addresses': addresses,
    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

