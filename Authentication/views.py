from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os


def login_user(request):
    """
    This method validate the user and login
    :param request: Type of request (GET or POST)
    :return: Login page
    """
    if request.method == 'POST':
        request.session['username'] = request.POST.get('username')
        password = request.POST.get('password')
        username = request.session.get('username')
        request.session['username'] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            context = {'username': username}
            login(request, user)
            return render(request, 'index.html', context)
        else:
            context = {
                'text': 'Invalid Username or Password'
            }
            messages.success(request, 'Invalid Username or Password')
            return render(request, 'login.html', context)
    if request.user.is_authenticated:
        context = {'username': request.session.get('username')}
        return render(request, 'index.html', context)
    else:
        return render(request, 'login.html')


@login_required
def logout_user(request):
    """
    This method logout the user
    :param request: Type of request (GET or POST)
    :return: Logout page
    """
    logout(request)
    return render(request, 'logout.html')


def forgot_password(request):
    context = {
        'password_change': True
    }
    return render(request, 'forgot_password.html', context)


def change_password(request):
    context = {
        'password_change': True
    }
    return render(request, 'change_password.html', context)


def change_password_ok(request):
    context = {
        'password_change_ok': True
    }
    return render(request, 'change_password_ok.html', context)







