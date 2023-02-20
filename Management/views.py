from django.shortcuts import render
import django
from Management.models import ProjectDetails
from Management.models import RefCarbonfootprint
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.conf import settings
from Management.models import RefCarbonfootprint
from datetime import datetime

# Create your views here.


def index(request):
    # import ipdb
    # ipdb.set_trace()
    # if request.method == 'GET':
    #
    #     draft = request.POST.get("draft")
    #     completed = request.POST.get("completed")
    #
    #     input_data = {
    #         'draft': draft,
    #         'completed': completed,
    #     }
    #     context = {
    #         'input_data': input_data,
    #         'draft': draft,
    #         'completed': completed,
    #     }
    #     return render(request, 'index.html', context)
    return render(request, 'index.html')


import pandas as pd
import time
from datetime import datetime


def projectA(request):
    """
    Project Duration
    Project Details
    Project Roles
    Direct Impact Parameters
    Indirect Impact Parameters
    """
    session_data = get_session_data(request)
    user_data = User.objects.all()
    country_list = settings.COUNTRY_LIST

    if request.method == 'POST':
        start_date_build = request.POST.get('start_date_build')
        end_date_build = request.POST.get('end_date_build')
        start_date_run = request.POST.get('start_date_run')
        end_date_run = request.POST.get('end_date_run')
        pl_1 = request.POST.get('pl_1')
        ps = request.POST.get('ps')
        bu = request.POST.get('bu')
        role = request.POST.getlist('role')
        department = request.POST.get('department')
        development = request.POST.get('development')
        type_project = request.POST.get('type_project')
        name = request.POST.get('name')
        work_country = request.POST.get('work_country')
        WhichUserEquipment = request.POST.getlist('WhichUserEquipment')
        WhichIndustrialEquipment = request.POST.getlist('WhichIndustrialEquipment')
        WhichParametersImplemented = request.POST.getlist('WhichParametersImplemented')

        separate_role = ''
        separate_WhichUserEquipment = ''
        separate_WhichIndustrialEquipment = ''
        separate_WhichParametersImplemented = ''

        for i in role:
            separate_role = separate_role + i + ', '

        for i in WhichUserEquipment:
            separate_WhichUserEquipment = separate_WhichUserEquipment + i + ', '

        for i in WhichIndustrialEquipment:
            separate_WhichIndustrialEquipment = separate_WhichIndustrialEquipment + i + ', '

        for i in WhichParametersImplemented:
            separate_WhichParametersImplemented = separate_WhichParametersImplemented + i + ', '


        # Get all above data in session
        request.session['start_date_build'] = start_date_build
        request.session['end_date_build'] = end_date_build
        request.session['start_date_run'] = start_date_run
        request.session['end_date_run'] = end_date_run
        request.session['pl_1'] = pl_1
        request.session['ps'] = ps
        request.session['bu'] = bu
        request.session['role'] = separate_role
        request.session['type_project'] = type_project
        request.session['development'] = development
        request.session['department'] = department
        request.session['name'] = name
        request.session['work_country'] = work_country
        request.session['WhichUserEquipment'] = separate_WhichUserEquipment
        request.session['WhichIndustrialEquipment'] = separate_WhichIndustrialEquipment
        request.session['WhichParametersImplemented'] = separate_WhichParametersImplemented

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        get_all_years = get_year(request, start_date_build, end_date_build, start_date_run, end_date_run)
        current_year = str(datetime.now()).split('-')[0]
        phase = get_current_phase(request, get_all_years, current_year)
        print(get_all_years)
        print(phase)
        request.session['current_phase'] = phase
        ProjectDetails_db = ProjectDetails.objects.all()
        print(ProjectDetails_db)

        # create_timestamp = time.ctime()
        # update_timestamp = time.ctime()
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        # print(update_timestamp)

        try:
            project_details_data = ProjectDetails(projectname=name,
                                                  projectlocation=pl_1,
                                                  department=department,
                                                  whichuserequipment=separate_WhichUserEquipment,
                                                  whichindustrialequipment=separate_WhichIndustrialEquipment,
                                                  buconcerned=bu,
                                                  projectstatus=ps,
                                                  phasetype=phase,
                                                  buildstartdate=start_date_build,
                                                  buildenddate=end_date_build,
                                                  runstartdate=start_date_run,
                                                  runenddate=end_date_run,
                                                  create_timestamp=create_timestamp,
                                                  update_timestamp=start_date_build,
                                                  whichindirectparameters=separate_WhichParametersImplemented,
                                                  projectrole=separate_role)
            project_details_data.save()
            print(project_details_data)
        except Exception as e:
            print("================================ Exception Raised during adding data in DB =======================")
            print(e)

        context = {
            'start_date_build': start_date_build,
            'end_date_build': end_date_build,
            'start_date_run': start_date_run,
            'end_date_run': end_date_run,
            'pl_1': pl_1,
            'ps': ps,
            'bu': bu,
            'department': department,
            'type_project': type_project,
            'name': name,
            'work_country': work_country,
            'WhichUserEquipment': WhichUserEquipment,
            'WhichIndustrialEquipment': WhichIndustrialEquipment,
            'WhichParametersImplemented': WhichParametersImplemented,
            'development': development,
            'role': role,
            'country_list': country_list,
            'progress_bar': True,
        }
        return render(request, 'load_plan.html', context)
    context = {
        'progress_bar': True,
        'country_list': country_list,
    }
    return render(request, 'projectA.html', context)


def company_detail(request):
    return render(request, 'company_detail.html')


def get_year(request, build_start_date, build_end_date, run_start_date, run_end_date):
    # import ipdb
    # ipdb.set_trace()
    build_start_date_year = build_start_date.split('-')[0]
    build_end_date_year = build_end_date.split('-')[0]
    run_start_date_year = run_start_date.split('-')[0]
    run_end_date_year = run_end_date.split('-')[0]

    return build_start_date_year, build_end_date_year, run_start_date_year, run_end_date_year


def get_current_phase(request, all_years, current_year):

    build_start_year = all_years[0]
    build_end_year = all_years[1]

    run_start_year = all_years[2]
    run_end_year = all_years[3]

    current_year = current_year

    build_year_list = []

    get_build_num_of_year = int(build_end_year) - int(build_start_year)
    for i in range(get_build_num_of_year + 1):
        build_year_list.append(int(build_start_year) + i)

    print('Build Year list: ', build_year_list)

    run_year_list = []

    get_run_num_of_year = int(run_end_year) - int(run_start_year)
    for i in range(get_run_num_of_year + 1):
        run_year_list.append(int(run_start_year) + i)

    print('Run Year list: ', run_year_list)

    if int(current_year) in build_year_list:
        phase = 'Build Phase'
    else:
        phase = 'Run Phase'

    print('Current Phase is: ', phase)

    return phase

def emission_lib(request):
    i = [1, 2]
    get_emission_library = get_emission_library_data(request)
    context = {
        'i': i,
        'progress_bar': True,
        'emission_library_list': get_emission_library
    }
    return render(request, 'emission_lib.html', context)


def datacenter_network(request):
    i = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    context = {
        'i': i,
    }
    return render(request, 'datacenter_network.html', context)


def indirect_impact_fl(request):
    return render(request, 'indirect_impact_fl.html')


def indirect_impact_el(request):
    return render(request, 'indirect_impact_el.html')


def load_plan(request):
    return render(request, 'load_plan.html')


def di_daily_commute(request):
    return render(request, 'di_daily_commute.html')


def di_business_travel(request):  
    return render(request, 'di_business_travel.html')


def Help(request):
    return render(request, 'Help.html')


def Indirect_Impact(request):
    context = {
        'progress_bar': True,
    }
    return render(request, 'Indirect_Impact.html', context)


def indirect_impact_mc(request):
    return render(request, 'indirect_impact_mc.html')


def indirect_impact_wt(request):
    return render(request, 'indirect_impact_wt.html')


def test_graph(request):
    get_emission_library = get_emission_library_data(request)
    context = {
        'progress_bar': True,
        'emission_library_list': get_emission_library
    }
    return render(request, 'temp.html', context)


def get_session_data(request):
    session_data = ProjectDetails.objects.all()
    dict_count = 1
    session_dict = {}
    for items in session_data:
        session_dict['session_dict_{}'.format(dict_count)] = items.__dict__
        session_dict.get('session_dict_{}'.format(dict_count))['_state'] = str(
            session_dict.get('session_dict_{}'.format(dict_count))['_state'])
        session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'] = \
            session_dict.get('session_dict_{}'.format(dict_count))['create_timestamp'].strftime("%d %B %Y")
        session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'] = \
            session_dict.get('session_dict_{}'.format(dict_count))['update_timestamp'].strftime("%d %B %Y")
        dict_count += 1
    return session_dict


def get_user_groups(request):
    user_groups = Group.objects.all()
    user_groups_dict = []
    for instance in user_groups:
        user_groups_dict.append(instance.__dict__)
    return user_groups_dict


def get_emission_library_data(request):
    emission_library_data = RefCarbonfootprint.objects.all()
    emission_library_data_list = []
    for item in emission_library_data:
        emission_library_data_list.append(item.__dict__)
    return emission_library_data_list




def error_400(request, exception):
    return render(request, '400.html')


def error_403(request, exception):
    return render(request, '403.html')


def error_404(request, exception):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')



