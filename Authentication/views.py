from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Management.models import ProjectDetails
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

        # Get all data of project details from DB
        # import ipdb
        # ipdb.set_trace()
        pro_details_dict = []
        pro_details_single_list = []
        session_dict = {}
        pro_details = ProjectDetails.objects.all()

        for instance in pro_details:
            pro_details_dict.append(instance.__dict__)

        for item in pro_details_dict:
            pro_details_single_list.append(item)
        len_db = len(pro_details)
        request.session['len_db'] = len_db
        # request.session['pro_details'] = pro_details
        # request.session['pro_details_single_'] = pro_details_single_list
        dict_count = 1
        for items in pro_details:
            session_dict['session_dict_{}'.format(dict_count)] = items.__dict__
            session_dict.get('session_dict_{}'.format(dict_count))['_state'] = str(session_dict.get('session_dict_{}'.format(dict_count))['_state'])
            session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'] = session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'].strftime("%d %B %Y")
            session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'] = session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'].strftime("%d %B %Y")
            dict_count += 1
        # import ipdb
        # ipdb.set_trace()
        print(pro_details)
        if user is not None:
            context = {'username': username, 'db_instance': len(pro_details), 'session_dict': session_dict}
            login(request, user)
            return render(request, 'index.html', context)
        else:
            context = {
                'text': 'Invalid Username or Password'
            }
            messages.success(request, 'Invalid Username or Password')
            return render(request, 'login.html', context)
    if request.user.is_authenticated:
        pro_details_dict = []
        pro_details_single_list = []
        pro_details = ProjectDetails.objects.all()
        session_dict = {}

     
        for instance in pro_details:
            pro_details_dict.append(instance.__dict__)

        for item in pro_details_dict:
            pro_details_single_list.append(item)
        len_db = len(pro_details)
        request.session['len_db'] = len_db
        # request.session['pro_details'] = pro_details
        # request.session['pro_details_single_'] = pro_details_single_list
        dict_count = 1
        for items in pro_details:
            session_dict['session_dict_{}'.format(dict_count)] = items.__dict__
            session_dict.get('session_dict_{}'.format(dict_count))['_state'] = str(
                session_dict.get('session_dict_{}'.format(dict_count))['_state'])
            session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'] = \
            session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'].strftime("%d %B %Y")
            session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'] = \
            session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'].strftime("%d %B %Y")
            dict_count += 1
        # import ipdb
        # ipdb.set_trace()
        print(pro_details)
        context = {'username': request.session.get('username'), 'db_instance': request.session.get('len_db'), 'session_dict': session_dict}
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









