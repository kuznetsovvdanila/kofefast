from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index_page(request):
    form = None

    if request.method == 'POST':
        if request.POST.get('action_type') == 'authen':
            password = request.POST.get('password1')
            username = request.POST.get('username')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')

    context = {
        'form': form if form else UserCreationForm(),
    }
    return render(request, 'pages/index.html', context)
