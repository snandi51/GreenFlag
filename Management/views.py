from django.shortcuts import render
import django
from Management.models import ProjectDetails
from Management.models import RefCarbonfootprint
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.conf import settings
from Management.models import RefCarbonfootprint, ImpactsDirects ,ImpactsIndirects
from datetime import datetime
from Management.models import LoadPlan
from django.forms.models import model_to_dict
import pyodbc
from Management.models import ProjectDetails, ImpactsDirects, ImpactsIndirects
from django.db.models import Count, Sum
import copy
import numpy as np


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
from datetime import date
from GreenFlag.settings import DATABASES



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
        request.session['start_date_build'] = start_date_build
        end_date_build = request.POST.get('end_date_build')
        request.session['end_date_build'] = end_date_build

        start_date_run = request.POST.get('start_date_run')
        request.session['start_date_run'] = start_date_run
        end_date_run = request.POST.get('end_date_run')

        request.session['end_date_run'] = end_date_run

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
        print(separate_role)

        for i in WhichUserEquipment:
            separate_WhichUserEquipment = separate_WhichUserEquipment + i + ', '

        for i in WhichIndustrialEquipment:
            separate_WhichIndustrialEquipment = separate_WhichIndustrialEquipment + i + ', '

        for i in WhichParametersImplemented:
            separate_WhichParametersImplemented = separate_WhichParametersImplemented + i + ', '

        # Get all above data in session
        request.session['user_equipment'] = WhichUserEquipment
        request.session['industrial_equipment'] = WhichIndustrialEquipment
        request.session['parameters_implemented'] = WhichParametersImplemented
        request.session['start_date_build'] = start_date_build
        request.session['end_date_build'] = end_date_build
        request.session['start_date_run'] = start_date_run
        request.session['end_date_run'] = end_date_run
        request.session['pl_1'] = pl_1
        request.session['ps'] = ps
        request.session['bu'] = bu
        request.session['role'] = role
        request.session['separate_role'] = separate_role
        request.session['type_project'] = type_project
        request.session['development'] = development
        request.session['department'] = department
        request.session['name'] = name
        request.session['work_country'] = work_country
        request.session['WhichUserEquipment'] = separate_WhichUserEquipment
        request.session['WhichIndustrialEquipment'] = separate_WhichIndustrialEquipment
        request.session['WhichParametersImplemented'] = separate_WhichParametersImplemented

        print('selected roles are:', role)

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

        # pro_manager = request.POST.get('pro_manager')
        # proxy = request.POST.get('proxy')
        # data = request.POST.get('data')
        # it_1 = request.POST.get('it_1')
        # it_2 = request.POST.get('it_2')
        # it_front = request.POST.get('it_front')
        # director = request.POST.get('director')
        # project = request.POST.get('project')
        role = request.POST.get('role')

        WhichUserEquipment = request.POST.get('WhichUserEquipment')
        # laptop = request.POST.get('laptop')
        # pc = request.POST.get('pc')
        # tablet = request.POST.get('tablet')
        # telephone = request.POST.get('telephone ')
        # printer = request.POST.get('printer')
        # speaker = request.POST.get('speaker')
        # projector = request.POST.get('projector')
        # monitor = request.POST.get('monitor')

        WhichIndustrialEquipment = request.POST.get('WhichIndustrialEquipment')
        # laptop1 = request.POST.get('laptop1')
        # camera = request.POST.get('camera')
        # sensor = request.POST.get('sensor')
        # lidar = request.POST.get('lidar')

        WhichParametersImplemented = request.POST.get('WhichParametersImplemented')
        # fuel = request.POST.get('fuel')
        # electricity = request.POST.get('electricity')
        # water = request.POST.get('water')
        # paper = request.POST.get('paper')
        # plastic = request.POST.get('plastic')
        # waste_material = request.POST.get('waste_material')
        # raw_material = request.POST.get('raw_material')
        # import ipdb
        # ipdb.set_trace()

        # create_timestamp = time.ctime()
        # update_timestamp = time.ctime()
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        # print(update_timestamp)

        # calculate start and End Year by using start_date_build and end_date_build for Build State
        start_date_build_year = start_date_build
        start_date_split = start_date_build_year.split('-')
        start_date_year = int(start_date_split[0])
        print(start_date_year)
        request.session["start_date_year"] = start_date_year
        start_date_year = request.session.get('start_date_year')

        start_date_month = int(start_date_split[1])
        print(start_date_month)
        # import ipdb
        # ipdb.set_trace()
        # quater_1 = []

        # get_quarter = lambda dt: (dt.month-1)//3 + 1
        # qu = lambda dt: (dt.start_date_month - 1)//3+1
        # print(qu)

        # quarter_to = get_quarter(end_date_build)
        # # print('quarter_from', quarter_from)
        # print('quarter_to', quarter_to)

        end_date_build_year = end_date_build
        end_date_split = end_date_build_year.split('-')
        end_date_year = int(end_date_split[0])
        print(end_date_year)
        request.session["end_date_year"] = end_date_year
        end_date_year = request.session.get('end_date_year')
        # build end month
        end_date_month = int(end_date_split[1])
        print(end_date_month)
        request.session["end_date_month"] = end_date_month

        totalyear = (end_date_year - start_date_year + 1)
        request.session["totalyear"] = totalyear
        totalyear = request.session.get('totalyear')
        print(totalyear)
        Quater = int(totalyear * 4)
        request.session['Quater'] = Quater
        Quater = request.session.get('Quater')
        print(Quater)

        totalyear_loop = []
        start_date_year = start_date_year
        for i in range(1, totalyear):
            start_date_year = start_date_year + 1
            totalyear_loop.append(start_date_year)
        print('totalyear_loop:', totalyear_loop)
        request.session["totalyear_loop"] = totalyear_loop

        count_year = (len(totalyear_loop)+1)
        print('count_year:', count_year)
        request.session["count_year"] = count_year

        # request.session["totalyear_loop"] = totalyear_loop
        # for r in range(1, totalyear + 1):
        #     totalyear_loop.append(r)
        # print(totalyear_loop)
        list = []
        list_count = []
        for i in range(1, Quater + 1):
            list.append(i)
        print('list:', list)
        request.session["list"] = list

        len1 = int(len(list)/4)
        a = 4
        c = 0
        for i in range(len1):
            list_count[c:a] = [1, 2, 3, 4]
            c = a
            a *= 4
        print('count_list:', list_count)
        request.session["list_count"] = list_count

        which_quater = (start_date_month - 1) // 3 + 1
        print("which_quater", which_quater)
        quarter_build_list = ''
        span_build_list = 0
        if which_quater == 1:
            quarter_build_list = 'q1'
            span_build_list = 0
        elif which_quater == 2:
            quarter_build_list = 'q2'
            span_build_list = 1
        elif which_quater == 3:
            quarter_build_list = 'q3'
            span_build_list = 2
        elif which_quater == 4:
            quarter_build_list = 'q4'
            span_build_list = 3
        print("quarter_build_list:", quarter_build_list)
        request.session["quarter_build_list"] = quarter_build_list
        print("span_build_list:", span_build_list)
        request.session["span_build_list"] = span_build_list

        which_quater_end_build = (end_date_month - 1) // 3 + 1
        print("which_quater_end_build", which_quater_end_build)

        which_quater_end_build = (end_date_month - 1) // 3 + 1
        print("which_quater_end_build", which_quater_end_build)
        # import ipdb; ipdb.set_trace()
        quarter_buildend_list = ''
        span_buildend_list = 0
        second_build_end_span = 0
        if which_quater_end_build == 1:
            quarter_buildend_list = 'q1'
            span_buildend_list = 6
        elif which_quater_end_build == 2:
            quarter_buildend_list = 'q2'
            span_buildend_list = 6
        elif which_quater_end_build == 3:
            quarter_buildend_list = 'q3'
            span_buildend_list = 3
        elif which_quater_end_build == 4:
            quarter_buildend_list = 'q4'
            span_buildend_list = 4

        if span_build_list == 0:
            second_build_end_span = 4
        elif span_build_list == 1:
            second_build_end_span = 5
        elif span_build_list == 2:
            second_build_end_span = 6
        elif span_build_list == 3:
            second_build_end_span = 8
        print("second_build_end_span:", second_build_end_span)
        request.session["second_build_end_span"] = second_build_end_span
        print("quarter_buildend_list:", quarter_buildend_list)
        request.session["quarter_buildend_list"] = quarter_buildend_list
        print("span_buildend_list:", span_buildend_list)
        request.session["span_buildend_list"] = span_buildend_list

        build_list = []
        for i in range(1, span_build_list + 1):
            build_list.append(i)
        print('build_list:', build_list)
        request.session["build_list"] = build_list

        # calculate start and End Year by using start_date_build and end_date_build for Run phase

        start_date_run_year = start_date_run
        start_date_split_run = start_date_run_year.split('-')
        start_date_year_run = int(start_date_split_run[0])
        print(start_date_year_run)
        request.session["start_date_year_run"] = start_date_year_run
        start_date_year_run = request.session.get('start_date_year_run')

        start_date_month_run = int(start_date_split_run[1])
        print(start_date_month_run)

        # Run colgroup to hide quater:
        which_quater_run = (start_date_month_run - 1) // 3 + 1
        print("which_quater_run", which_quater_run)
        quarter_build_list_run = ''
        span_build_list_run = 0
        if which_quater_run == 1:
            quarter_build_list_run = 'q1'
            span_build_list_run = 0
        elif which_quater_run == 2:
            quarter_build_list_run = 'q2'
            span_build_list_run = 1
        elif which_quater_run == 3:
            quarter_build_list_run = 'q3'
            span_build_list_run = 2
        elif which_quater_run == 4:
            quarter_build_list_run = 'q4'
            span_build_list_run = 3
        print("quarter_build_list_run:", quarter_build_list_run)
        request.session["quarter_build_list"] = quarter_build_list_run
        print("span_build_list_run:", span_build_list_run)
        request.session["span_build_list_run"] = span_build_list_run

        end_date_run_year = end_date_run
        end_date_split_run = end_date_run_year.split('-')
        end_date_year_run = int(end_date_split_run[0])
        print(end_date_year_run)
        request.session["end_date_year_run"] = end_date_year_run
        end_date_year_run = request.session.get('end_date_year_run')

        totalyear_run = (end_date_year_run - start_date_year_run + 1)
        request.session["totalyear_run"] = totalyear_run
        totalyear_run = request.session.get('totalyear_run')
        print(totalyear_run)
        Quater_run = int(totalyear_run * 4)
        request.session['Quater_run'] = Quater_run
        Quater_run = request.session.get('Quater_run')
        print(Quater_run)

        totalyear_loop_run = []
        start_date_year_run = start_date_year_run

        for i in range(1, totalyear_run):
            start_date_year_run = start_date_year_run + 1
            totalyear_loop_run.append(start_date_year_run)
        print('totalyear_loop_run', totalyear_loop_run)

        request.session['totalyear_loop_run'] = totalyear_loop

        list_run = []
        list_count_run = []
        for i in range(1, Quater_run + 1):
            list_run.append(i)
        print(list_run)
        request.session["list_run"] = list_run

        len2 = int(len(list_run)/4)
        b = 4
        d = 0
        for i in range(len2):
            list_run[d:b] = [1, 2, 3, 4]
            d = b
            b *= 4
        print('list_run:', list_run)
        request.session["list_run"] = list_run


        role_list = ['Project Manager', 'IT Leader 1']
        request.session['role_list'] = role_list
        print('role_list', role_list)

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
            current_project_id = project_details_data.projid
            request.session['current_project_id'] = current_project_id
        except Exception as e:
            print("================================ Exception Raised during adding data in DB =======================")
            print(e)

        context = {
            'build_list': request.session.get('build_list'),
            'end_date_month': request.session.get('end_date_month'),
            'span_build_list': request.session.get('span_build_list'),
            'quarter_build_list': request.session.get('quarter_build_list'),
            'span_buildend_list': request.session.get('span_buildend_list'),
            'quarter_buildend_list': request.session.get('quarter_buildend_list'),
            'span_build_list_run': request.session.get('span_build_list_run'),
            'count_year': request.session.get('count_year'),
            'second_build_end_span': request.session.get('second_build_end_span'),
            'start_date_build': request.session.get('start_date_build'),
            'end_date_build': request.session.get('end_date_build'),
            'start_date_run': request.session.get('start_date_run'),
            'end_date_run': request.session.get('end_date_run'),
            'start_date_year': request.session.get('start_date_year'),
            'end_date_year': request.session.get('end_date_year'),
            'totalyear': request.session.get('totalyear'),
            'Quater': request.session.get('Quater'),
            'start_date_month': start_date_month,
            'start_date_year_run': request.session.get('start_date_year_run'),
            'end_date_year_run': request.session.get('end_date_year_run'),
            'totalyear_run': totalyear_run,
            'Quater_run': Quater_run,
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_run': request.session.get('list_run'),
            'list_count_run':request.session.get('list_count_run'),
            'pl_1': pl_1,
            'ps': ps,
            'bu': bu,
            'department': department,
            'type_project': type_project,
            'name': name,
            'list': request.session.get('list'),
            'work_country': request.session.get('work_country'),
            'list_count': request.session.get('list_count'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'role_list': request.session.get('role_list'),
            # 'quater_1': quater_1,
            # 'pro_manager': pro_manager,
            # 'proxy': proxy,
            # 'data': data,
            # 'it_1': it_1,
            # 'it_2': it_2,
            # 'it_front': it_front,
            # 'director': director,
            # 'project': project,
            'WhichUserEquipment': WhichUserEquipment,
            'WhichIndustrialEquipment': WhichIndustrialEquipment,
            'WhichParametersImplemented': WhichParametersImplemented,
            'development': development,
            'role': request.session.get('role'),
            'country_list': country_list,
            'progress_bar': True,
            'phase_type' : request.session.get('phase_type'),
            'current_project_id' : request.session.get('current_project_id'),
        }
        return render(request, 'load_plan.html', context)


    totalyear = request.session.get('totalyear')  
    context = {
        'progress_bar': True,
        'country_list': country_list,
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'totalyear': totalyear,
        'phase_type' : request.session.get('phase_type'),
        'current_project_id' : request.session.get('current_project_id'),
    }
    return render(request, 'projectA.html', context)


def load_plan(request):
    if request.method == 'POST':
        # Build Phase for load plan screen:
        totalyear = request.session.get('totalyear')
        print('totalyear', totalyear)
        totalyear_len = len(range(totalyear))
        print('totalyear_len', totalyear_len)
        list_new = request.session.get('list')
        print('list_new', list_new)
        list_length = len(list_new)
        print('list_length', list_length)
        request.session['list_length'] = list_length
        phase_type = request.session.get('phase_type')
        role = request.session.get('role')
        len_role_list = len(role)
        print('list_length', list_length)
        len_totalrolelist = len(role) * list_length
        print('len_totalrolelist: ', len_totalrolelist)


       

        final_quater = []
        noofworkingdays_build2 = []
        noofworkingdays_run = []
        noofworkingdays_list = []
        # import ipdb
        # ipdb.set_trace()

        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            local_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                local_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('local_list', local_list)
                if local_list == ['']:
                    local_list = ['0']
                    # print('local_list', local_list)
                    print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in local_list:
                    if i == '':
                        local_list[count] = '0'
                        print('i', i)
                    count += 1

                print(local_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # local_list=[int(i) for i in local_list]
            # print('local_list', local_list)
            # local_list =sum(local_list)
           
            print('local_list', local_list)
            # import ipdb
            # ipdb.set_trace()

            
            noofworkingdays_build2.append(local_list)
            print('noofworkingdays_build2', noofworkingdays_build2)

            noofworkingdays_build=[]
            noofworkingdays_build1 = [i for list1 in noofworkingdays_build2 for i in list1]
            noofworkingdays_build1 =[int(i) for i in noofworkingdays_build1]
            if noofworkingdays_build1:
                noofworkingdays_build1 = sum(noofworkingdays_build1)
                noofworkingdays_build.append(noofworkingdays_build1)
            print('noofworkingdays_build',noofworkingdays_build)
            
            request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_list.append(noofworkingdays_build)
            
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        # RUN
        final_quater = []
        noofworkingdays_run2 = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            local_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                local_list.append(request.POST.get('run'+role[j-1] + '_' + str(i)))
                print('local_list', local_list)
                if local_list == ['']:
                    local_list = ['0']
                    # print('local_list', local_list)
                    print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in local_list:
                    if i == '':
                        local_list[count] = '0'
                        print('i', i)
                    count += 1

                print(local_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # local_list=[int(i) for i in local_list]
            # print('local_list', local_list)
            # local_list =sum(local_list)
           
            # print('local_list', local_list)

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            # import ipdb
            # ipdb.set_trace()
            noofworkingdays_run2.append(local_list)
            print('noofworkingdays_run2', noofworkingdays_run2)

            noofworkingdays_run=[]
            noofworkingdays_run1 = [i for list1 in noofworkingdays_run2 for i in list1]
            noofworkingdays_run1 =[int(i) for i in noofworkingdays_run1]
            if noofworkingdays_run1:
                noofworkingdays_run1 = sum(noofworkingdays_run1)
                noofworkingdays_run.append(noofworkingdays_run1)
            print('noofworkingdays_run',noofworkingdays_run)
            request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

    

        

        # Database entry:
        start_date_year = request.session.get('start_date_build')
        print(start_date_year)
        end_date_year = request.session.get('end_date_build')
        print(end_date_year)
        start_date_year_run = request.session.get('start_date_run')
        print(start_date_year_run)
        end_date_year_run = request.session.get('end_date_run')
        print(end_date_year_run)
        start_date_year = request.session.get('start_date_year')
        totalyear_loop_run = request.session.get('totalyear_loop_run')
        totalyear_loop = request.session.get('totalyear_loop')
        # Run phase screen:
        list_run = request.session.get('list_run')
        print('list_run', list_run)
        list_run_length = len(list_run)
        print('list_run_length', list_run_length)

        # noofworkingdays_run = []
        # # import ipdb
        # # ipdb.set_trace()
        # # Create user input field and append in list:
        # for k in range(1, len(role_list) + 1):
        #     print(k)
        #     local_list_run = []
        #     quater_list_run = []
        #     for l in range(1, list_run_length + 1):
        #         name = (request.POST.get('run' + role_list[k-1] + '_' + str(l)))
        #         print("name:", name)
        #         local_list_run.append(request.POST.get('run' + role_list[k-1] + '_' + str(l)))
        #         print('local_list_run', local_list_run)
        #         quater_list_run.append(l)
        #
        #     print('local_list_run', local_list_run)
        #     noofworkingdays_run.append(local_list_run)
        #     print('noofworkingdays_run', noofworkingdays_run)
        #     request.session['noofworkingdays_run'] = noofworkingdays_run

        # This data need to take from project detail screens:
        name = 'Snehal'
        work_country = request.session.get('work_country')
        typeofemployee = 'x'
        phasetype = 'run'
        year = 2022
        noofresources = 5
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")



        



        # To create object in database table:
        # load_plan_db = LoadPlan.objects.all()
        # print(load_plan_db)
        # # import ipdb
        # # ipdb.set_trace()
        # # To Generate ForeignKey from Project Details table:
        # user_detail = pd.DataFrame(list(ProjectDetails.objects.all().values('projid')))
        # print('user_detail', user_detail)
        # user_detail_dict = user_detail.to_dict('records')[-1]
        # print('user_detail_dict', user_detail_dict)
        # user_detail_id = user_detail_dict['projid']

        # import ipdb
        # ipdb.set_trace()
        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))
        
        # roleid.save()

        # request.session['roleid'] = roleid
        # print('this is type', type(roleid))
        # import ipdb
        # ipdb.set_trace()
        # Creating datagframe for role and workingday value to pass in database:

        # wd_df = pd.DataFrame(
        #     {'role': role,
        #      'wd': noofworkingdays_build,
        #      # 'wd_run': noofworkingdays_run,
        #      # 'quater': final_quater,
        #      # 'wd_final': noofworkingdays_list,
        #      })

        # print('wd_df', wd_df)

        # import ipdb
        # ipdb.set_trace()

        try:
            # for i, row in wd_df.iterrows():
            #     for working_day in row.wd:
                    print(working_day)
                    LoadPlan_data = LoadPlan(role=row.role, name=name, workcountry=work_country,
                                             typeofemployee=typeofemployee,
                                             phasetype=phase_type,
                                             noofworkingdays=working_day,
                                             buildstartdate=start_date_year, buildenddate=end_date_year,
                                             runstartdate=start_date_year_run, runenddate=end_date_year_run,
                                             create_timestamp=create_timestamp,
                                             update_timestamp=start_date_year, year=year, quarter=2,
                                             noofresources=noofresources, projid=roleid),

                    LoadPlan_data.save()
                    print(LoadPlan_data)
        except Exception as e:
            print(e)

        
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        # for i in daily_commute:
        #     print(i)
        # print(daily_commute)
        context = {
            'noofworkingdays_build': request.session.get('noofworkingdays_build'),
            'noofworkingdays_run': request.session.get('noofworkingdays_run'),
            'noofworkingdays_list': request.session.get('noofworkingdays_list'),
            'role': request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'start_date_year': request.session.get('start_date_year'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'daily_commute': daily_commute,
            'phase_type' : request.session.get('phase_type'),
            # 'roleid' : request.session.get('roleid'),
            
        }
        return render(request, 'di_daily_commute.html', context)
    start_date_year = request.session.get('start_date_year')
    totalyear_loop_run = request.session.get('totalyear_loop_run')
    totalyear_loop = request.session.get('totalyear_loop')
    # import ipdb
    # ipdb.set_trace()
    role = request.session.get('role'),
    phase_type = request.session.get('phase_type'),
    context={
        'role': request.session.get('role'),
        'noofworkingdays_list': request.session.get('noofworkingdays_list'),
        'list_run': request.session.get('list_run'),
        'list': request.session.get('list'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'phase_type' : request.session.get('phase_type'),
        # 'roleid' : request.session.get('roleid'),
        'noofworkingdays_build': request.session.get('noofworkingdays_build'),
            
    }
    return render(request, 'load_plan.html',context)

def di_daily_commute(request):
    
    if request.method == 'POST':
        # import ipdb
        # ipdb.set_trace()
        noofworkingdays_build = request.session.get('noofworkingdays_build')
        noofworkingdays_run = request.session.get('noofworkingdays_run')
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        end_date_year = request.session.get('end_date_year')
        end_date_year_run = request.session.get('end_date_year_run')
        phase_type = request.session.get('phase_type'),
        print(role)

        # mydata = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        # print(mydata)


        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        
        
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        # for i in daily_commute:
        #     print(i)
        # print(daily_commute)
       
        
        
        km_buildlist=[]    
        km_runlist=[]
        avg_runlist=[]
        avg_buildlist=[]
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)

            km_buildlist.append(request.POST.get(role[k-1]))
            print('km_buildlist',km_buildlist)
            avg_buildlist.append(request.POST.get('av_' + role[k-1]))
            print('avg_buildlist',avg_buildlist)
            km_runlist.append(request.POST.get('km_run_' + role[k-1]))
            print('km_runlist',km_runlist)
            avg_runlist.append(request.POST.get('avg_run_' + role[k-1]))
            print('avg_runlist',avg_runlist)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        # print('data type', type(km_buildlist[0]))

        
        # build phase total carbon calculations for Daily Commute
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        
        emission_factor_list =[]
        for i in transport_type:
            tt = ref_parameters_list.filter(subcategory= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['emissionfactor'])
            emission_factor_list.append(tt_lists[0]['emissionfactor'])
            print('emission_factor_list',emission_factor_list)


            
        # import ipdb
        # ipdb.set_trace()
        # emission_factor_list = [i.get('emissionfactor') for i in ref_parameters_list]
        # print(emission_factor_list)
        # for i in ref_parameters_list :
            
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')
       
        
        buid_km_int=[int(i) for i in km_buildlist]
        buid_km_int = [i * 2 for i in buid_km_int]
        print('buid_km_int',buid_km_int)
        buid_avg_int=[int(i) for i in avg_buildlist]
        num = 5
        # buid_avg_int= np.divide(buid_avg_int, num)
        
        buid_avg_int = [x / num for x in buid_avg_int]
        print('buid_avg_int',buid_avg_int)
        
        build1 = [(buid_avg_int[i])*((noofworkingdays_build[i])) for i in range(len(noofworkingdays_build))]
        print('build1',build1)
        # build1= build1[0]
        # print('build1',build1)
            
        run_km_int=[int(i) for i in km_runlist]
        print('run_km_int',run_km_int)
        run_avg_int=[int(i) for i in avg_runlist]
        print('run_avg_int',run_avg_int)
        emission_run = [run_km_int[i] * run_avg_int[i] for i in range(len(run_avg_int))]

        res_list = [build1[i] * buid_km_int[i] for i in range(len(buid_km_int))]
        print('res_list',res_list)

        totalcarbonfootprint_daily_build= [res_list[i] * emission_factor_list[i] for i in range(len(res_list))]
        print('totalcarbonfootprint_daily_build',totalcarbonfootprint_daily_build)


        # Run

        emission_factor_list_run =[]
        for i in transport_type_run:
            tt = ref_parameters_list.filter(subcategory= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['emissionfactor'])
            emission_factor_list_run.append(tt_lists[0]['emissionfactor'])
            print('emission_factor_list_run',emission_factor_list_run)

        # import ipdb
        # ipdb.set_trace()

        run_km_int=[int(i) for i in km_runlist]
        run_km_int = [i * 2 for i in run_km_int]
        print('run_km_int',run_km_int)
        run_avg_int=[int(i) for i in avg_runlist]
        num = 5
        # buid_avg_int= np.divide(buid_avg_int, num)

        run_avg_int = [x / num for x in run_avg_int]
        print('run_avg_int',run_avg_int)
        
        build2 = [(run_avg_int[i])*(int(noofworkingdays_run[i])) for i in range(len(noofworkingdays_run))]
        print('build2',build2)
        # build1= build1[0]
        # print('build1',build1)
            
        run_km_int=[int(i) for i in km_runlist]
        print('run_km_int',run_km_int)
        run_avg_int=[int(i) for i in avg_runlist]
        print('run_avg_int',run_avg_int)
        emission_run = [run_km_int[i] * run_avg_int[i] for i in range(len(run_avg_int))]

        res_list1 = [build2[i] * run_km_int[i] for i in range(len(run_km_int))]
        print('res_list',res_list)

        totalcarbonfootprint_daily_run= [res_list1[i] * emission_factor_list_run[i] for i in range(len(res_list))]
        print('totalcarbonfootprint_daily_run',totalcarbonfootprint_daily_run)

        # import ipdb
        # ipdb.set_trace()

        # To Generate ForeignKey from Project Details table:
        # user_detail = pd.DataFrame(list(ProjectDetails.objects.all().values('projid')))
        # print('user_detail', user_detail)
        # user_detail_dict = user_detail.to_dict('records')[-1]
        # print('user_detail_dict', user_detail_dict)
        # user_detail_id = user_detail_dict['projid']
        # roleid = ProjectDetails.objects.get(projid=user_detail_id)
        # print(roleid)
        # roleid.save()

        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))
        
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        grid_emission_factor = RefCarbonfootprint.objects.values_list('emissionfactor')
        # grid_emission_factor = grid_emission_factor.filter(name = buildcountry).values()
        # grid_emission_factor = pd.DataFrame(list(grid_emission_factor)) 
        # grid_emission_factor = grid_emission_factor['emissionfactor'][0]
        print('Grid emission factor',grid_emission_factor)

        grid_emission_factor_unit = RefCarbonfootprint.objects.values_list('unit')
        # grid_emission_factor_unit = grid_emission_factor.filter(name = buildcountry).values()
        # grid_emission_factor_unit = pd.DataFrame(list(grid_emission_factor))
        # grid_emission_factor_unit = grid_emission_factor['emissionfactor'][0]
        print('grid_emission_factor_unit',grid_emission_factor_unit)

        direct_impact_data = ImpactsDirects.objects.all()
        

        
        
        
        
        try:
                 for i in range(len(buid_km_int)):
                    
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            vehicleownership = vehical_owners[i],
                                            role = role[i],
                                            kmtravelledperday= buid_km_int[i],
                                            avgnoofdaysofficeperweek = buid_avg_int[i],
                                            category = 'People - Daily Commute',
                                            subcategory = transport_type[i],
                                            phasetype = 'Build',
                                            emissionfactor = emission_factor_list[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            typeoftransport = transport_type[i],
                                            projid = roleid,
                                            totalcarbonfootprint= totalcarbonfootprint_daily_build[i],
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)

                 for i in range(len(run_km_int)):
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            vehicleownership = vehical_owners[i],
                                            role = role[i],
                                            kmtravelledperday= run_km_int[i],
                                            avgnoofdaysofficeperweek = run_avg_int[i],
                                            category = 'People - Daily Commute',
                                            subcategory = transport_type[i],
                                            phasetype = 'Run',
                                            emissionfactor = emission_factor_list_run[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            typeoftransport = transport_type[i],
                                            projid = roleid,
                                            totalcarbonfootprint= totalcarbonfootprint_daily_run[i],
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)

        except Exception as e:
            print(e)
            print('=====================================================================Error================================================')










        # total_build=[]
        # ==============calculations=====
        # import ipdb
        # ipdb.set_trace()
        # dc_data =RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        # print('dc data',dc_data)
        # daily_em=[]
        # dc=[]
        # em_factor=[]
        # a=len(dc_data)
        # print('d4',a)
        # for i in range(a):
        #     # print(request.POST.get(str(i)))
        #     if request.POST.get('di' + str(i + 1)):
        #         daily_em.append(i + 1)
        # for index, row in dc_data.iterrows():
        #     if row['CarbonId'] in daily_em:
        #         em_factor.append(row['Unit'])
        # print('d1',daily_em)
        # print('d2',dc)
        # print('d3',em_factor)

        



        
        # build_mul=[]
        # for i in range(0, len(buid_km_int)):
        #     build_mul.append(buid_km_int[i] * buid_avg_int[i])
        # print('mul',build_mul)



        business_data_emission = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()

        # import ipdb
        # ipdb.set_trace()
        business_emission_list = []

        for i in business_data_emission:
            i.pop('carbonid')
            i.pop('name')
            i.pop('lcprod')
            i.pop('lctransport')
            i.pop('lcusage')
            i.pop('lcrecycling')
            i.pop('lifespanyrs')
            i.pop('carbonfootprintperday')
            i.pop('lcunit')
            i.pop('lcemissionfactor')
            i.pop('yearpublished')
            i.pop('projectusingef')
            i.pop('scope')
            i.pop('status')
            i.pop('typeofimpact')
            i.pop('update_timestamp')
            i.pop('create_timestamp')
            i.pop('projid_id')
            i.pop('category')
            i.pop('subcategory')
            i.pop('unit')
            business_emission_list.append(i)

        request.session['business_emission_list'] = business_emission_list

        




        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        phase_type = request.session.get('phase_type'),
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
            'phase_type' : request.session.get('phase_type'),
            'business_emission_list' : business_emission_list,
        } 
        return render(request, 'di_business_travel.html',context)
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    role=request.session.get('role')
    list=request.session.get('list')
    print('list1 is',list)
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    end_date_year = request.session.get('end_date_year')
    end_date_year_run = request.session.get('end_date_year_run')
    print(role)
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        
    # import ipdb
    # ipdb.set_trace()

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()


    # for i in daily_commute:
    #     print(i.subcategory)
    # import ipdb
    # ipdb.set_trace()
    # print(daily_commute)
    
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 
    context={
        'role':request.session.get('role'),
        'res_dct':res_dct,
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
        'fuel_data' : fuel_data,
        'business_emission_list' : business_emission_list,
    }
    return render(request, 'di_daily_commute.html',context)
    

def di_business_travel(request):  
    if request.method == 'POST':
        # import ipdb
        # ipdb.set_trace()
        
        phase_type = request.session.get('phase_type'),
        role=request.session.get('role')
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')


        user_equipment_render_list = copy.deepcopy(WhichUserEquipment)
        industrial_equipment_render_list = copy.deepcopy(WhichIndustrialEquipment)
        indirect_render_list = copy.deepcopy(WhichParametersImplemented)
        
        request.session['user_equipment_render_list'] = user_equipment_render_list
        request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
        request.session['indirect_render_list'] = indirect_render_list


        print('list1 is',list)
        totalyear_loop_run = request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        

        business_emission_list = request.session.get('business_emission_list')
        print(business_emission_list)

        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1
            
            Build_days_list=[int(i) for i in Build_days_list]
            print('Build_days_list', Build_days_list)
            Build_days_list =sum(Build_days_list)

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # import ipdb
            # ipdb.set_trace()

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
  

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        # noofworkingdays_build = request.session.get('noofworkingdays_build')
        
        final_quater = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

            Build_days_list=[int(i) for i in Build_days_list]
            print('Build_days_list', Build_days_list)
            Build_days_list =sum(Build_days_list)
                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
          

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        print('noofworkingdays_build', noofworkingdays_build)
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        # print('data type', type(km_buildlist[0]))
        
        ref_parameters_list_business = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        emission_factor_list =[]
        for i in transport_type:
            tt = ref_parameters_list_business.filter(subcategory= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['emissionfactor'])
            emission_factor_list.append(tt_lists[0]['emissionfactor'])
            print('emission_factor_list',emission_factor_list)

        # import ipdb
        # ipdb.set_trace()
        totalcarbonfootprint_business_build=[emission_factor_list[i] * noofworkingdays_build[i] for i in range(len(noofworkingdays_build))]
        print('totalcarbonfootprint_business_build',totalcarbonfootprint_business_build)
        

        emission_factor_list_run =[]
        for i in transport_type_run:
            tt = ref_parameters_list_business.filter(subcategory= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['emissionfactor'])
            emission_factor_list_run.append(tt_lists[0]['emissionfactor'])
            print('emission_factor_list_run',emission_factor_list_run)

        totalcarbonfootprint_business_run=[emission_factor_list_run[i] * noofworkingdays_run[i] for i in range(len(noofworkingdays_run))]
        print('totalcarbonfootprint_business_run',totalcarbonfootprint_business_run)

        total_noofworkingdays_run = sum(noofworkingdays_run)
        print('total_noofworkingdays_run',total_noofworkingdays_run)

        total_noofworkingdays_build = sum(noofworkingdays_build)
        print('total_noofworkingdays_build',total_noofworkingdays_build)



        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        print(laptop_data)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        country_list = settings.COUNTRY_LIST


        # buid_km_int=[int(i) for i in km_buildlist]
        # print(buid_km_int)
        # print('data type', type(buid_km_int[0]))
        # buid_avg_int=[int(i) for i in avg_buildlist]
        # print(buid_avg_int)


        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # import ipdb
        # ipdb.set_trace()

        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        for i in ref_parameters_list :
            
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        try:
                for i in range(len(transport_type)):
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            vehicleownership = vehical_owners[i],
                                            role = role[i],
                                            # kmtravelledperday= buid_km_int[0],
                                            # avgnoofdaysofficeperweek = buid_avg_int[0],
                                            category = 'People - Business Travel',
                                            subcategory = transport_type[i],
                                            phasetype ='Build',
                                            emissionfactor = emission_factor_list[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            typeoftransport = transport_type[i],
                                            projid = roleid,
                                            totalcarbonfootprint = totalcarbonfootprint_business_build[i],
                                            # nofworkingdays = total_noofworkingdays_build,
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)

                for i in range(len(transport_type)):
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            vehicleownership = vehical_owners_run[i],
                                            role = role[i],
                                            # kmtravelledperday= buid_km_int[0],
                                            # avgnoofdaysofficeperweek = buid_avg_int[0],
                                            category = 'People - Business Travel',
                                            subcategory = transport_type_run[i],
                                            phasetype ='Run',
                                            emissionfactor = emission_factor_list_run[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            typeoftransport = transport_type_run[i],
                                            projid = roleid,
                                            totalcarbonfootprint = totalcarbonfootprint_business_run[i],
                                            # nofworkingdays = total_noofworkingdays_run,
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)
        except Exception as e:
            print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()


        phase_type = request.session.get('phase_type'),
        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length' : request.session.get('list_length'),
            'laptop_data' :laptop_data,
            'country_list' : country_list,
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
            'fuel_data' : fuel_data,
        } 


        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 
    

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()




    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length' : request.session.get('list_length'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
        'fuel_data' : fuel_data,

    }
    return render(request, 'di_business_travel.html',context)

def di_laptop(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        noofworkingdays_build = request.session.get('noofworkingdays_build')
        noofworkingdays_run = request.session.get('noofworkingdays_run')
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
   
        
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
        work_country_run = []
        work_country = []

        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()

        # import ipdb
        # ipdb.set_trace()
        fuel_data_list = []

        for i in fuel_data:
            i.pop('carbonid')
            i.pop('name')
            i.pop('lcprod')
            i.pop('lctransport')
            i.pop('lcusage')
            i.pop('lcrecycling')
            i.pop('lifespanyrs')
            i.pop('emissionfactor')
            i.pop('carbonfootprintperday')
            i.pop('lcunit')
            i.pop('lcemissionfactor')
            i.pop('yearpublished')
            i.pop('projectusingef')
            i.pop('scope')
            i.pop('status')
            i.pop('typeofimpact')
            i.pop('update_timestamp')
            i.pop('create_timestamp')
            i.pop('projid_id')

            fuel_data_list.append(i)
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)
            work_country.append(request.POST.get('work_country_' + role[k-1]))
            print('work_country',work_country)
            work_country_run.append(request.POST.get('work_country_run_' + role[k-1]))
            print('work_country_run',work_country_run)
   

        # print('data type', type(km_buildlist[0]))
        
        ref_parameters_list_laptop = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        emission_factor_list =[]
        for i in transport_type:
            tt = ref_parameters_list_laptop.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list',emission_factor_list)

        totalcarbonfootprint_laptop_build = [emission_factor_list[i] * noofworkingdays_build[i] for i in range(len(noofworkingdays_build))]
        print('totalcarbonfootprint_laptop_build',totalcarbonfootprint_laptop_build)
     
        # import ipdb
        # ipdb.set_trace()

        emission_factor_list_run =[]
        for i in transport_type_run:
            tt = ref_parameters_list_laptop.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list_run.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list_run',emission_factor_list_run)

        totalcarbonfootprint_laptop_run = [emission_factor_list_run[i] * noofworkingdays_run[i] for i in range(len(noofworkingdays_run))]
        print('totalcarbonfootprint_laptop_run',totalcarbonfootprint_laptop_run)
        
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        try:
                for i in range(len(transport_type_run)):
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            # equipmentownership = vehical_owners[i],
                                            role = role[i],
                                            category = 'User Equipment',
                                            # typeoflaptop = transport_type[i],
                                            phasetype ='Build',
                                            emissionfactor = emission_factor_list_run[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            workcountry = work_country[i],
                                            totalcarbonfootprint = totalcarbonfootprint_laptop_run[i],
                                            projid = roleid,
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)
        except Exception as e:
            print(e)
   
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'electricity_data' : electricity_data,
            'fuel_data' : fuel_data,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
            'fuel_data_list' : fuel_data_list,
        } 


    

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'fuel_data' : fuel_data,
        'electricity_data' :electricity_data,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
    }
    return render(request, 'di_laptop.html',context)




def di_monitor(request): 
    # import ipdb
    # ipdb.set_trace()
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)
            
        # import ipdb
        # ipdb.set_trace()
        
    
        noofworkingdays_build_int =[int(i) for i in noofworkingdays_build]
        noofworkingdays_build_int = sum(noofworkingdays_build) 


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
            request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        # import ipdb
        # ipdb.set_trace()
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))

        ref_parameters_list_pc = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        emission_factor_list =[]
        for i in transport_type:
            tt = ref_parameters_list_pc.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list',emission_factor_list)

        totalcarbonfootprint_drone_build = [emission_factor_list[i] * noofworkingdays_build[i] for i in range(len(noofworkingdays_build))]
        print('totalcarbonfootprint_laptop_build',totalcarbonfootprint_laptop_build)
     
        # import ipdb
        # ipdb.set_trace()

        ref_parameters_list_pc_run =[]
        for i in transport_type_run:
            tt = ref_parameters_list_laptop.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list_run.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list_run',emission_factor_list_run)

        totalcarbonfootprint_laptop_run = [emission_factor_list_run[i] * noofworkingdays_run[i] for i in range(len(noofworkingdays_run))]
        print('totalcarbonfootprint_laptop_run',totalcarbonfootprint_laptop_run)


        # now = datetime.now()
        # create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # direct_impact_data = ImpactsDirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        # for i in ref_parameters_list :
        #     import ipdb
        #     ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        try:
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            equipmentownership = vehical_owners,
                                            role = role,
                                            # kmtravelledperday= buid_km_int[0],
                                            # avgnoofdaysofficeperweek = buid_avg_int[0],
                                            category = 'User Equipment',
                                            subcategory = transport_type[0],
                                            phasetype ='Build',
                                            emissionfactor = emissionfactor,
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            # typeoftransport = transport_type[0],
                                            # workcountry = work_country
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)
        except Exception as e:
            print(e)
        
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'fuel_data' : fuel_data,
            'electricity_data' : electricity_data,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
        }

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()


    context={
        'user_details':user_details,
        'year_details':year_details,
        'res_dct':res_dct,
        'default_dropdown1':default_dropdown1,
        'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'fuel_data' : fuel_data,
        'electricity_data' : electricity_data,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
       
    }
 
    return render(request, 'di_monitor.html',context)


def di_drone(request): 
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            request.session['noofworkingdays_drone'] = noofworkingdays_drone

            final_quater.append(quater_list)
            # print('final_quater', final_quater)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
            request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)



        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()

        # import ipdb
        # ipdb.set_trace()
        fuel_data_list = []

        for i in fuel_data:
            i.pop('carbonid')
            i.pop('name')
            i.pop('lcprod')
            i.pop('lctransport')
            i.pop('lcusage')
            i.pop('lcrecycling')
            i.pop('lifespanyrs')
            i.pop('emissionfactor')
            i.pop('carbonfootprintperday')
            i.pop('lcunit')
            i.pop('lcemissionfactor')
            i.pop('yearpublished')
            i.pop('projectusingef')
            i.pop('scope')
            i.pop('status')
            i.pop('typeofimpact')
            i.pop('update_timestamp')
            i.pop('create_timestamp')
            i.pop('projid_id')

            fuel_data_list.append(i)

        # import ipdb
        # ipdb.set_trace()
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)
        
        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        try:
                    IMPACTS_DIRECTS_data = ImpactsDirects(
                                            projectname = request.session.get('name'),
                                            equipmentownership = vehical_owners,
                                            role = role,
                                            projid = roleid,
                                            # kmtravelledperday= buid_km_int[0],
                                            # avgnoofdaysofficeperweek = buid_avg_int[0],
                                            category = 'Industrial Equipment',
                                            subcategory = transport_type[0],
                                            phasetype ='run',
                                            emissionfactor = emissionfactor,
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            # typeoftransport = transport_type[0],
                                            # workcountry = work_country
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_DIRECTS_data.save()
                    print(IMPACTS_DIRECTS_data)
        except Exception as e:
            print(e)

        list_length= request.session.get('list_length')

        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()


        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'fuel_data' : fuel_data,
            'fuel_data_list': fuel_data_list,
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'electricity_data' :electricity_data,
            'camera_data' : camera_data,
            'raw_data' : raw_data
        } 

        # import ipdb
        # ipdb.set_trace()

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
        # if WhichParametersImplemented[0]=='indirect_impact_fl':
        #     return render(request, 'indirect_impact_fl.html',context)
        # return render(request, 'di_raspberrypi.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
    list_length= request.session.get('list_length') 

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'fuel_data_list': fuel_data_list,
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'electricity_data' :electricity_data,
        'fuel_data' : fuel_data,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
    }
    return render(request, 'di_drone.html',context)

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


def indirect_impact_el(request):
    # import ipdb
    # ipdb.set_trace()
    submit = 0
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        print(role)


        noofworkingdays_build = []
        noofworkingdays_run = []
        
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        
        for i in range(1, list_length + 1):
            noofworkingdays_run.append(request.POST.get(str(i)))
            print('noofworkingdays_run', noofworkingdays_run)
            if noofworkingdays_run == ['']:
                noofworkingdays_run = ['0']
                    # print('local_list', local_list)
                print('noofworkingdays_run', noofworkingdays_run)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)
                # count = 0
                # for i in local_list:
                #     if i == '':
                #         local_list[count] = '0'
                #         print('i', i)
                #     count += 1

                # print(local_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            print('noofworkingdays_run', noofworkingdays_run)

            # noofworkingdays_build.append(local_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_fuel.append(noofworkingdays_run)
            # print('noofworkingdays_fuel', noofworkingdays_fuel)
            # request.session['noofworkingdays_fuel'] = noofworkingdays_fuel

            # final_quater.append(quater_list)
            # print('final_quater', final_quater)

        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()

        # import ipdb
        # ipdb.set_trace()
        fuel_data_list = []

        for i in fuel_data:
            i.pop('carbonid')
            i.pop('name')
            i.pop('lcprod')
            i.pop('lctransport')
            i.pop('lcusage')
            i.pop('lcrecycling')
            i.pop('lifespanyrs')
            i.pop('emissionfactor')
            i.pop('carbonfootprintperday')
            i.pop('lcunit')
            i.pop('lcemissionfactor')
            i.pop('yearpublished')
            i.pop('projectusingef')
            i.pop('scope')
            i.pop('status')
            i.pop('typeofimpact')
            i.pop('update_timestamp')
            i.pop('create_timestamp')
            i.pop('projid_id')

            fuel_data_list.append(i)

        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        paper_data = RefCarbonfootprint.objects.filter(category='Paper').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        submit = 1
        
        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)




        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'fuel_data_list' : fuel_data_list,
            'paper_data' : paper_data,
            'submit': submit,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
            'fuel_data' : fuel_data,
        } 

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'electricity_data' : electricity_data,
        'submit': submit,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
        'fuel_data' : fuel_data,
    }
    return render(request, 'indirect_impact_el.html',context)














def di_dcn(request):  
    return render(request, 'di_dcn.html')

def Help(request):
    return render(request, 'Help.html')


def Indirect_Impact(request):
    context = {
        'progress_bar': True,
    }
    return render(request, 'Indirect_Impact.html', context)



def indirect_impact_fl(request):
    submit = 0
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)

        
        noofworkingdays_build = []
        noofworkingdays_run = []
        
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        
        for i in range(1, list_length + 1):
            noofworkingdays_run.append(request.POST.get(str(i)))
            print('noofworkingdays_run', noofworkingdays_run)
            if noofworkingdays_run == ['']:
                noofworkingdays_run = ['0']
                    # print('local_list', local_list)
                print('noofworkingdays_run', noofworkingdays_run)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)
                # count = 0
                # for i in local_list:
                #     if i == '':
                #         local_list[count] = '0'
                #         print('i', i)
                #     count += 1

                # print(local_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            print('noofworkingdays_run', noofworkingdays_run)

            # noofworkingdays_build.append(local_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_fuel.append(noofworkingdays_run)
            # print('noofworkingdays_fuel', noofworkingdays_fuel)
            # request.session['noofworkingdays_fuel'] = noofworkingdays_fuel

            # final_quater.append(quater_list)
            # print('final_quater', final_quater)
        
        noofworkingdays_run1=[]
        Build_days_list=[int(i) for i in noofworkingdays_run]
        print('noofworkingdays_run', Build_days_list)
        noofworkingdays_run =sum(Build_days_list)
        noofworkingdays_run1.append(noofworkingdays_run)
        print('noofworkingdays_run1', noofworkingdays_run1)

       
        vehical_owners = []
        vehical_owners.append(request.POST.get('type_transport' ))
        print('vehical_owners',vehical_owners)
        ref_parameters_list_fuel = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        emission_factor_list =[]
        for i in vehical_owners:
            tt = ref_parameters_list_fuel.filter(subcategory= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['emissionfactor'])
            emission_factor_list.append(tt_lists[0]['emissionfactor'])
            print('emission_factor_list',emission_factor_list)

        totalcarbonfootprint_fuel = [emission_factor_list[i] * noofworkingdays_run1[i] for i in range(len(emission_factor_list))]
        print('totalcarbonfootprint_fuel',totalcarbonfootprint_fuel)



        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        el_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        country_list = settings.COUNTRY_LIST
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))
        # import ipdb
        # ipdb.set_trace()

        indirect_impact_data = ImpactsIndirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # for i in ref_parameters_list :
        #     import ipdb
        #     ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        try:
            for i in range(len(emission_factor_list)):
                    IMPACTS_INDIRECTS_data = ImpactsIndirects(
                                            projectname = request.session.get('name'),
                                            # equipmentownership = vehical_owners,
                                            # role = role,
                                            # kmtravelledperday= buid_km_int[0],
                                            # avgnoofdaysofficeperweek = buid_avg_int[0],
                                            category = 'Fuel - Stationary combustion',
                                            # subcategory = transport_type[0],
                                            phasetype ='Run',
                                            totalcarbonfootprint = totalcarbonfootprint_fuel[i],
                                            projid = roleid,
                                            emissionfactor = emission_factor_list[i],
                                            create_timestamp = create_timestamp,
                                            update_timestamp = create_timestamp,
                                            # typeoftransport = transport_type[0],
                                            # workcountry = work_country
                                            # buildstartdate=start_date_year, buildenddate=end_date_year,
                                            # runstartdate=start_date_year_run, runenddate=end_date_year_run,
                    )
                    IMPACTS_INDIRECTS_data.save()
                    print(ImpactsIndirects)
        except Exception as e:
            print(e)





        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        country_list = settings.COUNTRY_LIST
        print(pc_data)
        submit = 1
        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'el_data' : el_data,
            'country_list' : country_list,
            'pc_data' : pc_data,
            'electricity_data':electricity_data,
            'submit' : submit,
            'camera_data' : camera_data,
            'raw_data' : raw_data,
            'fuel_data' : fuel_data,
        } 
        # if len(WhichParametersImplemented)>=1:
        #  match WhichParametersImplemented[0]:
        #         case 'stationary_combustion':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_fl.html',context)
        #         case 'mobile_combustion':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_mc.html',context)
        #         case 'electricity':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_el.html',context)
        #         case 'water':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_wt.html',context) 
        #         case 'paper':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_paper.html',context)
        #         case 'waste_material':
        #             WhichParametersImplemented.pop(0)
        #             return render(request,'indirect_impact_wt.html',context)
        #         case 'raw_material':
        #             WhichParametersImplemented.pop(0)
        # import ipdb
        # ipdb.set_trace()

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)

        # return render(request, 'indirect_impact_el.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 

    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    print(camera_data)
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    country_list = settings.COUNTRY_LIST
    fuel_data_list = []

    for i in fuel_data:
        fuel_data_list.append(i)

    print('=========================================================')
    print(fuel_data_list)


    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'electricity_data': electricity_data,
        'country_list' : country_list,
        'submit' : submit,
        'camera_data' : camera_data,
        'raw_data' : raw_data,
        'fuel_data' : fuel_data,
    }
    return render(request, 'indirect_impact_fl.html',context)



def indirect_impact_mc(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        

        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)

        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_fuel' : request.session.get('noofworkingdays_fuel'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data
        }
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
          
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 

    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data
    }
    return render(request, 'indirect_impact_mc.html',context)





def indirect_impact_wt(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data
        } 
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 
    

    

    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data
    }
   
    return render(request, 'indirect_impact_wt.html',context)


def indirect_impact_waste(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data
        } 
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 

    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data,
    }
   
    return render(request, 'indirect_impact_waste.html',context)


def indirect_impact_rm(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data
        } 
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 
    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data
    }
   
    return render(request, 'indirect_impact_rm.html',context)

def indirect_impact_plastic(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]


        
        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data,
        } 
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 


    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data
    }
    return render(request, 'indirect_impact_plastic.html',context)

def indirect_impact_paper(request):
    if request.method=="POST":
        # import ipdb
        # ipdb.set_trace()
        
        role=request.session.get('role')
        list=request.session.get('list')
        print('list1 is',list)
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        print(role)
        default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        count = 1
        count2 = 1
        for i in range(len(default_dropdown)):
            default_dropdown.insert(count2, count)
            count+=1
            count2+=2
        res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        year_details=['2020','2021'] 
        quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
        user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        # indirect_impact_data = ImpactsIndirects.objects.all()
        # # ref_parameters_list = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        # # for i in ref_parameters_list :
        # #     import ipdb
        # #     ipdb.set_trace()
        # #     if i.get('subcategory') == transport_type[0]:
        # #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_INDIRECTS_data = ImpactsIndirects(
        #                                     projectname = request.session.get('name'),
        #                                     # equipmentownership = vehical_owners,
        #                                     # role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Fuel - Stationary combustion',
        #                                     # subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     totalcarbonfootprint = 20.0,
        #                                     projid = request.session.get('roleid'),
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_INDIRECTS_data.save()
        #             print(ImpactsIndirects)
        # except Exception as e:
        #     print(e)

        context={
            'user_details':user_details,
            'year_details':year_details,
            'res_dct':res_dct,
            'default_dropdown1':default_dropdown1,
            'quarter_details':quarter_details,
            'role':request.session.get('role'),
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
            'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
            'raw_data' : raw_data
        } 
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)  
    default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    count = 1
    count2 = 1

    # import ipdb
    # ipdb.set_trace()
    list=request.session.get('list')
    request.session['list']=list
    role=request.session.get('role')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    totalyear_loop= request.session.get('totalyear_loop')
    start_date_year = request.session.get('start_date_year')
    for i in range(len(default_dropdown)):
        default_dropdown.insert(count2, count)
        count+=1
        count2+=2
    res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    year_details=['2020','2021'] 
    quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4']
    user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',] 
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
    context={
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'totalyear_loop': request.session.get('totalyear_loop'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_drone' : request.session.get('noofworkingdays_drone'),
        'noofworkingdays_monitor' : request.session.get('noofworkingdays_monitor'),
        'raw_data': raw_data
    }
    return render(request, 'indirect_impact_paper.html',context)


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



def di_pc(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        # import ipdb
        # ipdb.set_trace()
        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)


        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        roleid = ProjectDetails.objects.get(projid=request.session.get('current_project_id'))

        # import ipdb
        # ipdb.set_trace()
        noofworkingdays_build2=[]
        noofworkingdays_build1 = [i for list1 in noofworkingdays_build for i in list1]
        noofworkingdays_build1 =[int(i) for i in noofworkingdays_build1]
        if noofworkingdays_build1:
            noofworkingdays_build1 = sum(noofworkingdays_build1)
            noofworkingdays_build2.append(noofworkingdays_build1)
        print('noofworkingdays_build',noofworkingdays_build)
        print('noofworkingdays_build1',noofworkingdays_build1)


        noofworkingdays_run2=[]
        noofworkingdays_run1 = [i for list1 in noofworkingdays_run for i in list1]
        noofworkingdays_run1 =[int(i) for i in noofworkingdays_run1]
        if noofworkingdays_run1:
            noofworkingdays_run1 = sum(noofworkingdays_run1)
            noofworkingdays_run1.append(noofworkingdays_run1)
        # print('noofworkingdays_build',noofworkingdays_build)
        print('noofworkingdays_run2',noofworkingdays_run2)

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list_desktop = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        
        
        emission_factor_list =[]
        for i in transport_type:
            tt = ref_parameters_list_desktop.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list',emission_factor_list)

        totalcarbonfootprint_desktop_build = [emission_factor_list[i] * noofworkingdays_build2[i] for i in range(len(noofworkingdays_build2))]
        print('totalcarbonfootprint_desktop_build',totalcarbonfootprint_desktop_build)

        emission_factor_list_run =[]
        for i in transport_type_run:
            tt = ref_parameters_list_desktop.filter(name= i).values()
            # tt = pd.DataFrame(list(tt))
            tt_lists = [i for i in tt]
            print(tt_lists[0]['carbonfootprintperday'])
            emission_factor_list_run.append(tt_lists[0]['carbonfootprintperday'])
            print('emission_factor_list_run',emission_factor_list_run)

        totalcarbonfootprint_desktop_run = [emission_factor_list_run[i] * noofworkingdays_run2[i] for i in range(len(noofworkingdays_build2))]
        print('totalcarbonfootprint_desktop_build',totalcarbonfootprint_desktop_build)



        # for i in ref_parameters_list :
        #     import ipdb
        #     ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        # try:
        #         for i in len()
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
        #                                     projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners[i],
        #                                     role = role[i],
        #                                     projid = roleid,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[i],
        #                                     phasetype ='run',
        #                                     emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     totalcarbonfootprint =
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        
        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data,
        }



        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)

    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data
       
    }
    return render(request, 'di_pc.html',context)

def di_tablet(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)



        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)

        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data
        }

   

        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
       
    }
    return render(request, 'di_tablet.html',context)

def di_telephone(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)


        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # direct_impact_data = ImpactsDirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        # for i in ref_parameters_list :
        #     # import ipdb
        #     # ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        # import ipdb
        # ipdb.set_trace()
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()   
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        
        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
    }
    return render(request, 'di_telephone.html',context)

def di_printer(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)


        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # direct_impact_data = ImpactsDirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        # for i in ref_parameters_list :
        #     # import ipdb
        #     # ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
       
    }
    return render(request, 'di_printer.html',context)

def di_bt_speaker(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)


        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)

        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        
        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data,
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
    }
    return render(request, 'di_bt_speaker.html',context)

def di_projector(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")


        # direct_impact_data = ImpactsDirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        # for i in ref_parameters_list :
        #     # import ipdb
        #     # ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'User Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data,
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'raw_data' : raw_data
    }
    return render(request, 'di_projector.html',context)

def di_camera(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)
        # import ipdb
        # ipdb.set_trace()

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        
        # direct_impact_data = ImpactsDirects.objects.all()
        # ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        # for i in ref_parameters_list :
        #     # import ipdb
        #     # ipdb.set_trace()
        #     if i.get('subcategory') == transport_type[0]:
        #         emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Industrial Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
        # print('camera_data',camera_data)
        fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        context={
           
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'sensor_data' : sensor_data,
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'electricity_data' :electricity_data,
            'fuel_data' : fuel_data,
            'camerat_data' : camera_data,
            'raw_data' : raw_data,
        }
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
        
        # return render(request, 'di_connected_sensor.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')


    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
    fuel_data = RefCarbonfootprint.objects.filter(category='Fuel - Stationary combustion').values()
    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    camera_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Camera').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()


    context={
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'sensor_data' : sensor_data,
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'electricity_data' :electricity_data,
        'fuel_data' : fuel_data,
        'camerat_data' : camera_data,
        'raw_data' : raw_data,
       
    }
    return render(request, 'di_camera.html',context)

def di_connected_sensor(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)
        # import ipdb
        # ipdb.set_trace()

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)

        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        
        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Industrial Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)


        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'sensor_data' : sensor_data,
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data,
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        # 'user_details':user_details,
        # 'year_details':year_details,
        # 'res_dct':res_dct,
        # 'default_dropdown1':default_dropdown1,
        # 'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'sensor_data' : sensor_data,
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
       
    }
    return render(request, 'di_connected_sensor.html',context)

def di_lidar(request): 
    if request.method == 'POST': 
        # import ipdb
        # ipdb.set_trace()
        list=request.session.get('list')
        WhichUserEquipment = request.session.get('user_equipment')
        WhichIndustrialEquipment = request.session.get('industrial_equipment')
        WhichParametersImplemented = request.session.get('parameters_implemented')
        role=request.session.get('role')
        totalyear_loop_run= request.session.get('totalyear_loop_run')
        start_date_year_run= request.session.get('start_date_year_run')
        totalyear_loop= request.session.get('totalyear_loop')
        start_date_year = request.session.get('start_date_year')
        
        # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
        # count = 1
        # count2 = 1
        # for i in range(len(default_dropdown)):
        #     default_dropdown.insert(count2, count)
        #     count+=1
        #     count2+=2
        # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
        # print(res_dct)
        # import ipdb
        # ipdb.set_trace()
        # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
        # year_details=['2020','2021']
        # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
        # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]
        role = request.session.get('role')


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_drone = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        # print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get(role[j-1] + '_' + str(i)))
                print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('local_list', local_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('dr_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            noofworkingdays_build.append(Build_days_list)
            print('noofworkingdays_build', noofworkingdays_build)
            

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            # noofworkingdays_drone.append(noofworkingdays_build)
            # print('noofworkingdays_drone', noofworkingdays_drone)
            

            final_quater.append(quater_list)
            # print('final_quater', final_quater)


        final_quater = []
        noofworkingdays_build = []
        noofworkingdays_run = []
        noofworkingdays_monitor = []
        # import ipdb
        # ipdb.set_trace()
        list_length= request.session.get('list_length')
        print(list_length)
        # Create user input field and append in list:
        for j in range(1, len(role) + 1):
            print(j)
            Build_days_list = []
            local_list_run = []
            quater_list = []
            for i in range(1, list_length + 1):
                Build_days_list.append(request.POST.get('bu_run_' + role[j-1] + '_' + str(i)))
                # print('Build_days_list', Build_days_list)
                if Build_days_list == ['']:
                    Build_days_list = ['0']
                    # print('local_list', local_list)
                    # print('Build_days_list', Build_days_list)
                # else:
                #     local_list.append(request.POST.get('run' + role_list[j-1] + '_' + str(i)))
                #     print('local_list', local_list)

                # local_list.append(request.POST.get('mo_' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                quater_list.append(i)
                count = 0
                for i in Build_days_list:
                    if i == '':
                        Build_days_list[count] = '0'
                        # print('i', i)
                    count += 1

                # print(Build_days_list)
                #
                # local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                # print('local_list', local_list)
                # quater_list.append(i)

            # print('Build_days_list', Build_days_list)

            # noofworkingdays_build.append(Build_days_list)
            # print('noofworkingdays_build', noofworkingdays_build)
            # request.session['noofworkingdays_build'] = noofworkingdays_build

            noofworkingdays_run.append(Build_days_list)
            print('noofworkingdays_run', noofworkingdays_run)
           

            # noofworkingdays_monitor.append(noofworkingdays_build)
            # print('noofworkingdays_monitor', noofworkingdays_monitor)
            # request.session['noofworkingdays_monitor'] = noofworkingdays_monitor

            final_quater.append(quater_list)
            print('final_quater', final_quater)
        # import ipdb
        # ipdb.set_trace()

        vehical_owners = []
        transport_type = []
        vehical_owners_run = []
        transport_type_run = []
    
        
        for k in range(1,len(role)+1):
            # print(k)
            vehical_owners.append(request.POST.get('vehical_ownership_' + role[k-1]))
            print('vehical',vehical_owners)
            transport_type.append(request.POST.get('type_transport_' + role[k-1]))
            print('transport_type',transport_type)
            vehical_owners_run.append(request.POST.get('vehical_ownership_run_' + role[k-1]))
            print('vehical_owners_run',vehical_owners_run)
            transport_type_run.append(request.POST.get('type_transport_run_' + role[k-1]))
            print('transport_type_run',transport_type_run)


        now = datetime.now()
        create_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        
        direct_impact_data = ImpactsDirects.objects.all()
        ref_parameters_list = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Lidar').values()
        for i in ref_parameters_list :
            # import ipdb
            # ipdb.set_trace()
            if i.get('subcategory') == transport_type[0]:
                emissionfactor = i.get('emissionfactor')


        # try:
        #             IMPACTS_DIRECTS_data = ImpactsDirects(
                                            # projectname = request.session.get('name'),
        #                                     equipmentownership = vehical_owners,
        #                                     role = role,
        #                                     # kmtravelledperday= buid_km_int[0],
        #                                     # avgnoofdaysofficeperweek = buid_avg_int[0],
        #                                     category = 'Industrial Equipment',
        #                                     subcategory = transport_type[0],
        #                                     phasetype ='run',
        #                                     # emissionfactor = emissionfactor,
        #                                     create_timestamp = create_timestamp,
        #                                     update_timestamp = create_timestamp,
        #                                     # typeoftransport = transport_type[0],
        #                                     # workcountry = work_country
        #                                     # buildstartdate=start_date_year, buildenddate=end_date_year,
        #                                     # runstartdate=start_date_year_run, runenddate=end_date_year_run,
        #             )
        #             IMPACTS_DIRECTS_data.save()
        #             print(IMPACTS_DIRECTS_data)
        # except Exception as e:
        #     print(e)

        country_list = settings.COUNTRY_LIST
        electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
        daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
        laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
        business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
        monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
        drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
        pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
        tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
        telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
        printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
        projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
        lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
        sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
        raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()
        # print(electricity_data)
        context={
            # 'user_details':user_details,
            # 'year_details':year_details,
            # 'res_dct':res_dct,
            # 'default_dropdown1':default_dropdown1,
            # 'quarter_details':quarter_details,
            'list': request.session.get('list'),
            'list_run': request.session.get('list_run'),
            'role': request.session.get('role'),
            'totalyear_loop': request.session.get('totalyear_loop'),
            'start_date_year': request.session.get('start_date_year'),
            'start_date_year_run': request.session.get('start_date_year_run'),
            'totalyear_loop_run': request.session.get('totalyear_loop_run'),
            'list_length': request.session.get('list_length'),
            'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
            'electricity_data' : electricity_data,
            'country_list' :country_list,
            'sensor_data' : sensor_data,
            'daily_commute' : daily_commute,
            'business_travel': business_travel,
            'laptop_data':laptop_data,
            'monitor_data':monitor_data,
            'drone_data': drone_data,
            'pc_data': pc_data,
            'telephone_data' : telephone_data,
            'printer_data' : printer_data,
            'projector_data' : projector_data,
            'lidar_data' : lidar_data,
            'tablet_data' : tablet_data,
            'raw_data' : raw_data,
        }
        
        user_equipment_render_list = request.session.get('user_equipment_render_list')
        industrial_equipment_render_list = request.session.get('industrial_equipment_render_list')
        indirect_render_list = request.session.get('indirect_render_list')

        # import ipdb
        # ipdb.set_trace()
        if len(user_equipment_render_list)>=1:
            
            # if WhichUserEquipment[0]=='laptop':
            #     return render(request,'di_laptop.html',context)
            if user_equipment_render_list[0] == 'laptop':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_laptop.html',context)
            elif user_equipment_render_list[0] == 'pc':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_pc.html',context)
            elif user_equipment_render_list[0] == 'tablet':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_tablet.html',context)
            elif user_equipment_render_list[0] == 'telephone':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_telephone.html',context)
            elif user_equipment_render_list[0] == 'projector':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_printer.html',context)
            elif user_equipment_render_list[0] == 'monitor':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_bt_speaker.html',context)
            elif user_equipment_render_list[0] == 'Video':
                user_equipment_render_list.pop(0)
                request.session['user_equipment_render_list'] = user_equipment_render_list
                return render(request,'di_projector.html',context)
            else:
                user_equipment_render_list.pop(0)
                return render(request,'di_monitor.html',context)
                request.session['user_equipment_render_list'] = user_equipment_render_list

            return render(request, 'di_laptop.html',context)
       
        elif len(industrial_equipment_render_list)>=1:

                if industrial_equipment_render_list[0] == 'drone':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_drone.html',context)
                elif industrial_equipment_render_list[0] == 'camera':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_camera.html',context)
                elif industrial_equipment_render_list[0] == 'sensor':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_connected_sensor.html',context)
                elif industrial_equipment_render_list[0] == 'lidar':
                    industrial_equipment_render_list.pop(0)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                    return render(request,'di_lidar',context) 
                else :
                    industrial_equipment_render_list.pop(0)
                    return render(request,'di_raspberrypi.html',context)
                    request.session['industrial_equipment_render_list'] =industrial_equipment_render_list
                return render(request, 'di_drone.html',context)


        else:
            if len(indirect_render_list)>=1:

                if indirect_render_list[0] == 'stationary_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_fl.html',context)
                elif 'mobile_combustion':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_mc.html',context)
                elif 'electricity':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_el.html',context)
                elif 'water':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context) 
                elif 'paper':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_paper.html',context)
                elif 'waste_material':
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_wt.html',context)
                else:
                    indirect_render_list.pop(0)
                    request.session['indirect_render_list'] = indirect_render_list
                    return render(request,'indirect_impact_rm.html',context)
                return render(request, 'di_drone.html',context)
    # default_dropdown=['Car', 'Metro', 'Airplane', 'Train','Metro1', ]   
    # count = 1
    # count2 = 1
    role=request.session.get('role')
    totalyear_loop= request.session.get('totalyear_loop')
    totalyear_loop_run= request.session.get('totalyear_loop_run')
    start_date_year_run= request.session.get('start_date_year_run')
    start_date_year = request.session.get('start_date_year')
    # for i in range(len(default_dropdown)):
    #     default_dropdown.insert(count2, count)
    #     count+=1
    #     count2+=2
    # res_dct = {default_dropdown[i]: default_dropdown[i + 1] for i in range(0, len(default_dropdown), 2)}
    # print(res_dct)
    # import ipdb
    # ipdb.set_trace()
    # default_dropdown1=['Car1', 'Metro1', 'Airplane1', 'Train1', ]
    # year_details=['2020','2021']
    # quarter_details=['Q1','Q2','Q3','Q4','Q1','Q2','Q3','Q4'] 
    # user_details=['Product Owner', 'Proxy PO', 'Data Scientist', 'IT Leader 1','IT Leader 2',]

    electricity_data = RefCarbonfootprint.objects.filter(category='Grid Electricity').values()
    daily_commute = RefCarbonfootprint.objects.filter(category='People - Daily commute').values()
    laptop_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Laptop').values()
    business_travel = RefCarbonfootprint.objects.filter(category='People- Business Travel').values()
    monitor_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Screen/Monitor').values()
    drone_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Drones').values()
    pc_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Desktop').values()
    tablet_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Tablet').values()
    telephone_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Telephone').values()
    printer_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Printer').values()
    projector_data = RefCarbonfootprint.objects.filter(category='User Equipment',subcategory='Video projector').values()
    lidar_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Lidar').values()
    sensor_data = RefCarbonfootprint.objects.filter(category='Industrial Equipment',subcategory='Connected Sensors').values()
    raw_data = RefCarbonfootprint.objects.filter(category='Raw Material').values()

    context={
        'user_details':user_details,
        'year_details':year_details,
        'res_dct':res_dct,
        'default_dropdown1':default_dropdown1,
        'quarter_details':quarter_details,
        'totalyear_loop': request.session.get('totalyear_loop'),
        'role':request.session.get('role'),
        'list': request.session.get('list'),
        'list_run': request.session.get('list_run'),
        'start_date_year': request.session.get('start_date_year'),
        'start_date_year_run': request.session.get('start_date_year_run'),
        'totalyear_loop_run': request.session.get('totalyear_loop_run'),
        'list_length': request.session.get('list_length'),
        'noofworkingdays_monitor': request.session.get('noofworkingdays_monitor'),
        'electricity_data' : electricity_data,
        'country_list' :country_list,
        'sensor_data' : sensor_data,
        'daily_commute' : daily_commute,
        'business_travel': business_travel,
        'laptop_data':laptop_data,
        'monitor_data':monitor_data,
        'drone_data': drone_data,
        'pc_data': pc_data,
        'telephone_data' : telephone_data,
        'printer_data' : printer_data,
        'projector_data' : projector_data,
        'lidar_data' : lidar_data,
        'tablet_data' : tablet_data,
        'raw_data' : raw_data,
       
    }
    return render(request, 'di_lidar.html',context)

def di_raspberrypi(request):
    return render(request, 'di_raspberrypi.html')



def detailed_view_cmo(request):
    # Change project id to dynamic project id after the code integration is complete

    # import ipdb
    # ipdb.set_trace()
    proj_id = 58
    projects_count = noofcols()
    result_dict = project_status()
    Status_list = result_dict['status_list']
    counts = result_dict['counts']
    dis = direct_impact_score()
    dis = dis['totalcarbonfootprint__sum']
    iis = indirect_impact_score()
    iis = iis['totalcarbonfootprint__sum']
    # dis = 0.044
    iis = 0.564
    ni = dis + iis
    roe = iis/dis
    # status = counts.keys()
    # status_count = counts.values()
    savco2 = savingsco2()
    gain = gainofInv()
    gain = gain['investmentindigitalprojects__sum']
    today = date.today()
    curr_year = today.year
    idcy, iidcy = curyearimpacts()
    nicy = idcy['totalcarbonfootprint__sum'] + iidcy['totalcarbonfootprint__sum']
    curyrempcnt = CompanyDetails.objects.filter(year=curr_year).values_list('noofemployees', flat=True)
    curyrempcnt = curyrempcnt[0]
    avgco2emp = nicy/curyrempcnt
    avgidemp = idcy['totalcarbonfootprint__sum']/curyrempcnt
    avgiidemp = iidcy['totalcarbonfootprint__sum']/curyrempcnt
    turnovercuryr = CompanyDetails.objects.filter(year=curr_year).values_list('turnover', flat=True)
    turnovercuryr = turnovercuryr[0]

    directimpactproj = dis/projects_count

    context = {
        'projects_count' : projects_count,
        'status_list': Status_list,
        'counts': counts,
        'dis': dis,
        'iis': iis,
        'ni': round(ni),
        'roe': round(roe,0),
        # 'savco2': round(savco2*iis,2),
        # 'gain' : round(savco2/gain, 2),
        'idcy': idcy['totalcarbonfootprint__sum'],
        'iidcy': iidcy['totalcarbonfootprint__sum'],
        'avgco2emp': round(avgco2emp,2),
        'avgco2proj': round(nicy/turnovercuryr,2),
        'avgco2turnover': round(nicy/turnovercuryr,2),
        'avgidemp' : avgidemp,
        'avgiidemp' : avgiidemp,
        'directimpactproj': round(directimpactproj,2),
        'directimpcuryremp' : round(idcy['totalcarbonfootprint__sum']/curyrempcnt,2),
        'directimpcuryturnover' : round(iidcy['totalcarbonfootprint__sum']/turnovercuryr,2),
        'indirectimpactproj': round(iis/projects_count, 2),
        'indirectimpcuryremp' : round(iidcy['totalcarbonfootprint__sum']/curyrempcnt,2),
        'indirectimpcuryturnover' : round(iidcy['totalcarbonfootprint__sum']/turnovercuryr,2),
    }
    return render(request, 'detailed_view_cmo.html', context)


def noofcols():
    return ProjectDetails.objects.all().count()


def project_status():
    # project = ProjectDetails.objects.all()
    result = (ProjectDetails.objects.values('projectstatus').annotate(dcount=Count('projid')).order_by())
    Status_list = []
    counts = []
    for row in result:
        Status_list.append(row['projectstatus'])
        counts.append(row['dcount'])
    # result_dict = dict(zip(Status_list, counts))
    result_dict = {
        'status_list': Status_list,
        'counts': counts
    }
    return result_dict


def savingsco2():
    # company_detail=
    today = date.today()
    curr_year = today.year
    company_details = CompanyDetails.objects.filter(year=curr_year).values_list('carbonprice', flat=True)
    carbon_price = company_details[0]
    return carbon_price


def gainofInv():
    return Company.objects.aggregate(Sum('investmentindigitalprojects'))


def direct_impact_score():
    return ImpactsDirects.objects.aggregate(Sum('totalcarbonfootprint'))


def indirect_impact_score():
    return ImpactsIndirects.objects.aggregate(Sum('totalcarbonfootprint'))

def curyearimpacts():
    today = date.today()
    curr_year = today.year
    impactsdirect = ImpactsDirects.objects.filter(year = curr_year)
    impactsindirect = ImpactsIndirects.objects.filter(year = curr_year)
    id_curryr=impactsdirect.aggregate(Sum('totalcarbonfootprint'))
    iid_curryr=impactsdirect.aggregate(Sum('totalcarbonfootprint'))
    return id_curryr,iid_curryr


def view_detailed_result(request):
    proj_id = 58
    projects_count = noofcols()
    result_dict = project_status()
    Status_list = result_dict['status_list']
    counts = result_dict['counts']
    dis = direct_impact_score()
    dis = dis['totalcarbonfootprint__sum']
    iis = indirect_impact_score()
    iis = iis['totalcarbonfootprint__sum']
    dis = 0.044
    name = request.session.get('name');
    iis = 0.564
    ni = dis + iis
    roe = round(iis / dis)
    tot_years = [1, 2, 3, 4, 6]
    year_values = [1, 2, 4, 5, 6, 7]
    avg_run_phase = get_avg_run_phase()
    avg_build_phase = get_avg_build_phase()
    avg_direct_impact_cal = avg_direct_impact()
    avg_indirect_impact_cal = avg_indirect_impact()
    # status = counts.keys()
    # status_count = counts.values()
    graph_table = {
        '2020': 0.4,
        '2021': 0.33,
        '2022': 0.24,
        '2023': 0.14,
    }
    context = {
        'projects_count': projects_count,
        'status_list': Status_list,
        'counts': counts,
        'avg_direct_impact_cal': avg_direct_impact_cal,
        'avg_indirect_impact_cal': avg_indirect_impact_cal,
        'avg_run_phase': avg_run_phase,
        'avg_build_phase': avg_build_phase,
        'tot_years': tot_years,
        'year_values': year_values,
        'dis': dis,
        'iis': iis,
        'name': name,
        'graph_table': graph_table,
        'ni': ni,
        'roe': roe
    }
    return render(request, 'view_detailed_result.html', context)


def get_avg_run_phase():
    avg_run_phase = 0
    return avg_run_phase


def get_avg_build_phase():
    avg_build_phase = 0
    return avg_build_phase


def avg_direct_impact():
    tot_direct_impacts = ImpactsDirects.objects.aggregate(Sum('kmtravelledperday'))
    avg_direct_impact_calculation = 0
    return tot_direct_impacts


def avg_indirect_impact():
    tot_indirect_impacts = ImpactsIndirects.objects.aggregate(Sum('totalcarbonfootprint'))
    avg_indirect_impact_calculation = 0
    return tot_indirect_impacts


def noofcols():
    return ProjectDetails.objects.all().count()


def project_status():
    # project = ProjectDetails.objects.all()
    result = (ProjectDetails.objects.values('projectstatus').annotate(dcount=Count('projid')).order_by())
    Status_list = []
    counts = []
    for row in result:
        Status_list.append(row['projectstatus'])
        counts.append(row['dcount'])
    # result_dict = dict(zip(Status_list, counts))
    result_dict = {
        'status_list': Status_list,
        'counts': counts
    }
    return result_dict

def draft_duplicate_project(request):
    project_id = request.GET.get('id')
    project_id_split = project_id.split('_')[2]
    context_data = get_index_context_data(request)
    context = {
        'session_dict': context_data,
        'db_instance': len(context_data)
    }
    print('Duplicate project id is', project_id_split)
    return render(request, 'index.html', context)


def draft_mark_as_complete_project(request):
    project_id = request.GET.get('id')
    project_id_split = project_id.split('_')[2]
    context_data = get_index_context_data(request)
    context = {
        'session_dict': context_data,
        'db_instance': len(context_data)
    }
    print('Mark as complete project id is', project_id_split)
    return render(request, 'index.html', context)

	
def draft_delete_project(request):
    context_data = get_index_context_data(request)
    context = {
        'session_dict': context_data,
        'db_instance': len(context_data)
    }
    project_id = request.GET.get('id')
    project_id_split = project_id.split('_')[2]
    print('Deleting project id is', project_id_split)
    return render(request, 'index.html', context)


