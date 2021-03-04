from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from PIL import Image
import numpy as np

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

    providers = Provider.objects.all()

    drinkable = []

    for provider in providers:
        for item in provider.item_set.all().filter(type='d'):
            if item.not_has_color:
                item.primary_color = ""
                img = Image.open(item.preview)
                img = img.resize((500, 500))
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

    context = {
        # 'items': Provider.item_set.all().filter(type='d'),
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
            adr = AddressUser(owner=request.user, city=request.POST.get('city'), street=request.POST.get('street'),
                              house=request.POST.get('house'))
            if request.POST.get('entrance'):
                adr.entrance = request.POST.get('entrance')

            print(adr)
            adr.save()
        if request.POST.get('action_type') == 'prefer_address':
            for i in request.user.chosen_address.all():
                request.user.chosen_address.remove(i)
            print(AddressUser.objects.all().filter(id=request.POST.get('prefered_adr_id'))[0])
            request.user.chosen_address.add(AddressUser.objects.all().filter(id=request.POST.get('prefered_adr_id'))[0])
            request.user.save()

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


def logoutUser(request):
    logout(request)
    return redirect('index')

