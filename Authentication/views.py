from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Management.models import ProjectDetails
from Management.models import ImpactsDirects, ImpactsIndirects
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
        session_dict_direct = {}
        session_dict_indirect = {}

        pro_details = ProjectDetails.objects.all()

        data_direct = ImpactsDirects.objects.all()
        print('data_direct:', data_direct)

        # data_indirect = ImpactsIndirects.objects.values('projectname')
        data_indirect = ImpactsIndirects.objects.all()
        print('data_indirect:', data_indirect)
        # import ipdb
        # ipdb.set_trace()
        data_direct_projectname = ImpactsDirects.objects.values('projectname')
        print('data_direct_projectname:', data_direct_projectname)

        data_direct_totalfootprint = ImpactsDirects.objects.values('totalcarbonfootprint')
        print('data_direct_totalfootprint:', data_direct_totalfootprint)

        data_indirect_footprint = ImpactsIndirects.objects.values('totalcarbonfootprint')
        print('data_indirect_footprint:', data_indirect_footprint)
        print(type(data_indirect_footprint))

        # import ipdb
        # ipdb.set_trace()

        list_data_direct = []
        for i in data_direct:
            list_data_direct.append(i.__dict__)
        total_count = 0
        # import ipdb
        # ipdb.set_trace()
        for i in data_direct:
            list_data_direct[total_count]['indirect_carbonfootprint'] = data_indirect_footprint[total_count].get('totalcarbonfootprint')
            list_data_direct[total_count]['Net_impact'] = data_indirect_footprint[total_count].get('totalcarbonfootprint') + data_direct_totalfootprint[total_count].get('totalcarbonfootprint')
            list_data_direct[total_count]['roe'] = round(data_direct_totalfootprint[total_count].get('totalcarbonfootprint') / list_data_direct[total_count]['Net_impact'], 2)
            total_count += 1
        # print('data_direct:', data_direct)

        for instance in pro_details:
            pro_details_dict.append(instance.__dict__)

        pro_detail_indirect = []
        pro_detail_direct = []
        for instance_direct in data_direct:
            pro_detail_direct.append(instance_direct.__dict__)

        for instance_indirect in data_indirect:
            pro_detail_indirect.append(instance_indirect.__dict__)

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
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_direct:', pro_detail_direct)
        print('pro_detail_indirect:', pro_detail_indirect)

        dict_count_direct = 1
        for items_direct in pro_detail_direct:
            session_dict_direct['session_dict_direct{}'.format(dict_count_direct)] = items_direct
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['_state'] = str(session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['_state'])
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['create_timestamp'] = session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['create_timestamp'].strftime("%d %B %Y")
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['update_timestamp'] = session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['update_timestamp'].strftime("%d %B %Y")
            dict_count_direct += 1
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_direct:', pro_detail_direct)

        dict_count_indirect = 1
        for items_indirect in pro_detail_indirect:
            session_dict_indirect['session_dict_indirect{}'.format(dict_count_indirect)] = items_indirect
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['_state'] = str(session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['_state'])
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['create_timestamp'] = session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['create_timestamp'].strftime("%d %B %Y")
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['update_timestamp'] = session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['update_timestamp'].strftime("%d %B %Y")
            dict_count_direct += 1
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_indirect:', pro_detail_indirect)

        pro_di = []

        for x in data_indirect_footprint:
            pro_detail_direct.append(x)

        # import ipdb
        # ipdb.set_trace()
        pro_di.append(pro_detail_direct)
        print('pro_di:', pro_di)

        dict_count_in_direct = 1
        session_dict_in_direct = {}
        # import ipdb
        # ipdb.set_trace()
        for items_in_direct in list_data_direct:
            session_dict_in_direct['session_dict_in_direct{}'.format(dict_count_in_direct)] = items_in_direct
            session_dict_in_direct.get('session_dict_in_direct{}'.format(dict_count_in_direct))['_state'] = str(session_dict_in_direct.get('session_dict_in_direct{}'.format(dict_count_in_direct))['_state'])
            dict_count_in_direct += 1

        print('session_dict_in_direct:', session_dict_in_direct)

        if user is not None:
            context = {'username': username, 'db_instance': len(pro_details), 'session_dict': session_dict, 'session_dict_direct': session_dict_direct,
                       'session_dict_indirect': session_dict_indirect, 'data_indirect_footprint': data_indirect_footprint, 'pro_di': pro_di, 'list_data_direct': list_data_direct,
                       'session_dict_in_direct': session_dict_in_direct}
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
        session_dict_direct = {}
        session_dict_indirect = {}

        pro_details = ProjectDetails.objects.all()

        data_direct = ImpactsDirects.objects.all()
        print('data_direct:', data_direct)

        # data_indirect_footprint = ImpactsIndirects.objects.values('totalcarbonfootprint')
        data_indirect = ImpactsIndirects.objects.all()
        print('data_indirect:', data_indirect)

        for instance in pro_details:
            pro_details_dict.append(instance.__dict__)

        pro_detail_indirect = []
        pro_detail_direct = []
        for instance_direct in data_direct:
            pro_detail_direct.append(instance_direct.__dict__)

        for instance_indirect in data_indirect:
            pro_detail_indirect.append(instance_indirect.__dict__)

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
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_direct:', pro_detail_direct)
        print('pro_detail_indirect:', pro_detail_indirect)
        data_indirect_footprint = ImpactsIndirects.objects.values('totalcarbonfootprint')

        data_direct_totalfootprint = ImpactsDirects.objects.values('totalcarbonfootprint')
        print('data_direct_totalfootprint:', data_direct_totalfootprint)

        list_data_direct = []
        for i in data_direct:
            list_data_direct.append(i.__dict__)
        total_count = 0
        for i in data_direct:
            list_data_direct[total_count]['indirect_carbonfootprint'] = data_indirect_footprint[total_count].get('totalcarbonfootprint')
            list_data_direct[total_count]['Net_impact'] = data_indirect_footprint[total_count].get('totalcarbonfootprint') + data_direct_totalfootprint[total_count].get('totalcarbonfootprint')
            list_data_direct[total_count]['roe'] = round(data_direct_totalfootprint[total_count].get('totalcarbonfootprint') / list_data_direct[total_count]['Net_impact'], 2)
            total_count += 1

        dict_count_direct = 1
        for items_direct in pro_detail_direct:
            session_dict_direct['session_dict_direct{}'.format(dict_count_direct)] = items_direct
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['_state'] = str(session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['_state'])
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['create_timestamp'] = session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['create_timestamp'].strftime("%d %B %Y")
            session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['update_timestamp'] = session_dict_direct.get('session_dict_direct{}'.format(dict_count_direct))['update_timestamp'].strftime("%d %B %Y")
            dict_count_direct += 1
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_direct:', pro_detail_direct)

        dict_count_indirect = 1
        for items_indirect in pro_detail_indirect:
            session_dict_indirect['session_dict_indirect{}'.format(dict_count_indirect)] = items_indirect
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['_state'] = str(session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['_state'])
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['create_timestamp'] = session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['create_timestamp'].strftime("%d %B %Y")
            session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['update_timestamp'] = session_dict_indirect.get('session_dict_indirect{}'.format(dict_count_indirect))['update_timestamp'].strftime("%d %B %Y")
            dict_count_direct += 1
        # import ipdb
        # ipdb.set_trace()
        print('pro_detail_indirect:', pro_detail_indirect)

        dict_count_in_direct = 1
        session_dict_in_direct = {}

        for items_in_direct in list_data_direct:
            session_dict_in_direct['session_dict_in_direct{}'.format(dict_count_in_direct)] = items_in_direct
            session_dict_in_direct.get('session_dict_in_direct{}'.format(dict_count_in_direct))['_state'] = str(session_dict_in_direct.get('session_dict_in_direct{}'.format(dict_count_in_direct))['_state'])
            dict_count_in_direct += 1

        print('session_dict_in_direct:', session_dict_in_direct)

        pro_di = []

        for x in data_indirect_footprint:
            pro_detail_direct.append(x)

        # import ipdb
        # ipdb.set_trace()
        pro_di.append(pro_detail_direct)
        print('pro_di:', pro_di)

        context = {'username': request.session.get('username'), 'db_instance': request.session.get('len_db'), 'session_dict': session_dict, 'session_dict_direct': session_dict_direct,
                   'session_dict_indirect': session_dict_indirect, 'data_indirect_footprint': data_indirect_footprint, 'pro_di': pro_di, 'list_data_direct': list_data_direct, 'session_dict_in_direct': session_dict_in_direct}
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