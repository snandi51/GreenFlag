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

        projectstatus = ProjectDetails.objects.filter(projectstatus='completed')
        print(projectstatus)

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

        dict_count_completed = 1
        session_dict_completed = {}
        for items_com in projectstatus:
            session_dict_completed['session_dict_completed{}'.format(dict_count_completed)] = items_com.__dict__
            session_dict_completed.get('session_dict_completed{}'.format(dict_count_completed))['_state'] = str(session_dict_completed.get('session_dict_completed{}'.format(dict_count_completed))['_state'])
            dict_count_completed += 1
        print('session_dict_completed:', session_dict_completed)

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

        list_data_comp = []
        for i in projectstatus:
            list_data_comp.append(i.__dict__)
        total_count_com = 0

        data_direct_totalfootprint = ImpactsDirects.objects.values('totalcarbonfootprint')
        print('data_direct_totalfootprint:', data_direct_totalfootprint)

        data_direct_directid = ImpactsDirects.objects.values('directid')
        print('data_direct_directid:', data_direct_directid)

        for i in projectstatus:
            list_data_comp[total_count_com]['indirect_carbonfootprint'] = data_indirect_footprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['direct_carbonfootprint'] = data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['directid'] = data_direct_directid[total_count_com].get('directid')
            list_data_comp[total_count_com]['Net_impact'] = data_indirect_footprint[total_count_com].get('totalcarbonfootprint') + data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['roe'] = round(data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint') / list_data_comp[total_count_com]['Net_impact'], 2)
            total_count_com += 1
        print('list_data_comp:', list_data_comp)

        session_list_new = {}
        dict_count_completed = 0
        for items_completed in list_data_comp:
            session_list_new['session_list_new{}'.format(dict_count_completed)] = items_completed
            session_list_new.get('session_list_new{}'.format(dict_count_completed))['_state'] = str(session_list_new.get('session_list_new{}'.format(dict_count_completed))['_state'])
            dict_count_completed += 1
        # import ipdb; ipdb.set_trace()
        # import ipdb; ipdb.set_trace()
        print('session_list_new:', session_list_new)
        # import ipdb
        # ipdb.set_trace()
        print(len(data_direct_projectname))

        if user is not None:
            context = {'username': username, 'db_instance': len(data_direct_projectname), 'session_dict': session_dict, 'session_dict_direct': session_dict_direct,
                       'session_dict_indirect': session_dict_indirect, 'data_indirect_footprint': data_indirect_footprint, 'pro_di': pro_di, 'list_data_direct': list_data_direct,
                       'session_dict_in_direct': session_dict_in_direct, 'session_dict_completed': session_dict_completed,
                       'session_list_new':session_list_new, 'db_compl_ins': len(projectstatus)}
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

        projectstatus = ProjectDetails.objects.filter(projectstatus='completed')
        print(projectstatus)

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

        dict_count_completed = 1
        session_dict_completed = {}
        for items_com in projectstatus:
            session_dict_completed['session_dict_completed{}'.format(dict_count_completed)] = items_com.__dict__
            session_dict_completed.get('session_dict_completed{}'.format(dict_count_completed))['_state'] = str(session_dict_completed.get('session_dict_completed{}'.format(dict_count_completed))['_state'])
            dict_count_completed += 1
        print('session_dict_completed:', session_dict_completed)

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

        data_direct_projectname = ImpactsDirects.objects.values('projectname')
        print('data_direct_projectname:', data_direct_projectname)

        pro_di.append(pro_detail_direct)
        print('pro_di:', pro_di)

        list_data_comp = []
        for i in projectstatus:
            list_data_comp.append(i.__dict__)
        total_count_com = 0

        data_direct_totalfootprint = ImpactsDirects.objects.values('totalcarbonfootprint')
        print('data_direct_totalfootprint:', data_direct_totalfootprint)

        for i in projectstatus:
            list_data_comp[total_count_com]['indirect_carbonfootprint'] = data_indirect_footprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['direct_carbonfootprint'] = data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['Net_impact'] = data_indirect_footprint[total_count_com].get('totalcarbonfootprint') + data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint')
            list_data_comp[total_count_com]['roe'] = round(data_direct_totalfootprint[total_count_com].get('totalcarbonfootprint') / list_data_comp[total_count_com]['Net_impact'], 2)
            total_count_com += 1
        print('list_data_comp:', list_data_comp)

        session_list_new = {}
        dict_count_completed = 0
        for items_completed in list_data_comp:
            session_list_new['session_list_new{}'.format(dict_count_completed)] = items_completed
            session_list_new.get('session_list_new{}'.format(dict_count_completed))['_state'] = str(session_list_new.get('session_list_new{}'.format(dict_count_completed))['_state'])
            dict_count_completed += 1

        print('session_list_new:', session_list_new)

        # y = '0'
        # if (projectstatus=='completed'):
        #     y = '1'
        # else:
        #     y = '2'

        context = {'username': request.session.get('username'), 'db_instance': len(data_direct_projectname), 'session_dict': session_dict, 'session_dict_direct': session_dict_direct,
                   'session_dict_indirect': session_dict_indirect, 'data_indirect_footprint': data_indirect_footprint, 'pro_di': pro_di, 'list_data_direct': list_data_direct, 'session_dict_in_direct': session_dict_in_direct,
                   'session_dict_completed': session_dict_completed, 'session_list_new': session_list_new, 'db_compl_ins': len(projectstatus)}
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