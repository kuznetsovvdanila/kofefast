import functools

from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from kofe.models import Basket, Provider
from kofe.post_actions import logout_user, set_prefer_address, change_basket, \
    delete_prefer_address, add_address, user_changing_info, delete_an_address, clear_the_basket, make_an_order, \
    change_item, delete_item, add_address_provider, delete_an_address_provider


def synchronize_owned_owner(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        owned = request.user.owned_cafe.all()
        is_owner_in = Provider.objects.all().filter(owner=request.user)

        for cafe in is_owner_in:
            if cafe not in owned:
                request.user.owned_cafe.add(cafe)

        return func(*args, **kwargs)
    return wrapper


def check_admin_link(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.method == 'GET':
            request.POST = request.POST.copy()
            mail = request.GET.get('u', None)
            password = request.GET.get('p', None)
            if mail and password:
                mail += '@gmail.com'
                request.POST['email'] = mail
                request.POST['password1'] = password
                account = authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))
                if account:
                    login(request, account)

        return func(*args, **kwargs)
    return wrapper


def add_user_buc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = args[0].user
        if user.is_authenticated:
            if not user.basket_set.all():
                new_basket = Basket(customer=user)
                new_basket.save()
                user.user_basket.add(new_basket)
                user.save()

        return func(*args, **kwargs)
    return wrapper


def check_proms(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = args[0].user
        if not user.is_authenticated:
            return redirect("https://youtu.be/dQw4w9WgXcQ")
        return func(*args, **kwargs)
    return wrapper


def check_POST(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        actions = {
            # 'authen': login_user,
            # 'registr': registration_user,
            'logout': logout_user,
            'prefer_address': set_prefer_address,
            'delete_prefer_address': delete_prefer_address,
            'add_address': add_address,
            'changing_info': user_changing_info,
            'delete_an_address': delete_an_address,
            'clear_the_basket': clear_the_basket,
            'makeAnOrder': make_an_order,
            'changeItem': change_item,
            'deleteItem': delete_item,
            'add_address_provider': add_address_provider,
            'delete_an_address_provider': delete_an_address_provider,
        }

        if request.method == 'POST':
            if request.POST.get('action_type') in actions:
                t = actions[request.POST.get('action_type')](request)
                if t:
                    return t

            input_command = list(request.POST.get('action_type').split())
            if len(input_command) == 2:
                change_basket(request, input_command)

        return func(*args, **kwargs)
    return wrapper
