from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from sklearn.cluster import KMeans

from kofe.models import Provider


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
            #if item.not_has_color:
                #def palette(clusters):
                #    width = 300
                #    palette = np.zeros((50, width, 3), np.uint8)
                #    steps = width / clusters.cluster_centers_.shape[0]
                #    for idx, centers in enumerate(clusters.cluster_centers_):
                #        palette[:, int(idx * steps):(int((idx + 1) * steps)), :] = centers
                #    return palette

                #clt_3 = KMeans(n_clusters=3)
                #clt_3.fit(img_2.reshape(-1, 3))
                #show_img_compar(img_2, palette(clt_3))
            drinkable.append(item)

    context = {
        'providers': Provider.objects.all(),
        'drinks': drinkable,
        'form': form if form else UserCreationForm(),
        'errors': errors
    }
    print(len(drinkable))
    return render(request, 'pages/index.html', context)


def personal_area_page(request):
    context = {

    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

