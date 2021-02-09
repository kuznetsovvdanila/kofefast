from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


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

    context = {
        'form': form if form else UserCreationForm(),
        'errors': errors
    }
    return render(request, 'pages/index.html', context)


def personal_area_page(request):
    context = {

    }
    return render(request, 'pages/personal_area.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

