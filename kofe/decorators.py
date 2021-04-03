import functools

from django.shortcuts import redirect

from kofe.models import Basket
from kofe.post_actions import login_user, registration_user, logout_user, set_prefer_address, change_basket, \
    delete_prefer_address, add_address, user_changing_info, delete_an_address


def add_user_buc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = args[0].user
        if user.is_authenticated:
            if not user.basket_set.all():
                print("here")
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
            'authen': login_user,
            'registr': registration_user,
            'logout': logout_user,
            'prefer_address': set_prefer_address,
            'delete_prefer_address': delete_prefer_address,
            'add_address': add_address,
            'changing_info': user_changing_info,
            'delete_an_address': delete_an_address,
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
