from django.shortcuts import render
import django
from Management.models import ProjectDetails
from Management.models import RefCarbonfootprint
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.conf import settings
from Management.models import RefCarbonfootprint
from datetime import datetime
from Management.models import LoadPlan
from django.forms.models import model_to_dict
import pyodbc

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
            'totalyear_loop_run': totalyear_loop_run,
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
        }
        return render(request, 'load_plan.html', context)
    context = {
        'progress_bar': True,
        'country_list': country_list,
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

        role = request.session.get('role')
        len_role_list = len(role)

        len_totalrolelist = len(role) * list_length
        print('len_totalrolelist: ', len_totalrolelist)

        final_quater = []
        noofworkingdays_build = []
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

                local_list.append(request.POST.get('run' + role[j-1] + '_' + str(i)))
                print('local_list', local_list)
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

            print('local_list', local_list)

            noofworkingdays_build.append(local_list)
            print('noofworkingdays_build', noofworkingdays_build)
            request.session['noofworkingdays_build'] = noofworkingdays_build

            # noofworkingdays_run.append(local_list)
            # print('noofworkingdays_run', noofworkingdays_run)
            # request.session['noofworkingdays_run'] = noofworkingdays_run

            noofworkingdays_list.append(noofworkingdays_build)
            print('noofworkingdays_list', noofworkingdays_list)
            request.session['noofworkingdays_list'] = noofworkingdays_list

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
        load_plan_db = LoadPlan.objects.all()
        print(load_plan_db)
        # import ipdb
        # ipdb.set_trace()
        # To Generate ForeignKey from Project Details table:
        user_detail = pd.DataFrame(list(ProjectDetails.objects.all().values('projid')))
        print('user_detail', user_detail)
        user_detail_dict = user_detail.to_dict('records')[-1]
        print('user_detail_dict', user_detail_dict)
        user_detail_id = user_detail_dict['projid']
        roleid = ProjectDetails.objects.get(projid=user_detail_id)
        print(roleid)
        roleid.save()

        # import ipdb
        # ipdb.set_trace()
        # Creating datagframe for role and workingday value to pass in database:

        wd_df = pd.DataFrame(
            {'role': role,
             'wd': noofworkingdays_build,
             # 'wd_run': noofworkingdays_run,
             # 'quater': final_quater,
             # 'wd_final': noofworkingdays_list,
             })

        print('wd_df', wd_df)

        try:
            for i, row in wd_df.iterrows():
                for working_day in row.wd:
                    print(working_day)
                    LoadPlan_data = LoadPlan(role=row.role, name=name, workcountry=work_country,
                                             typeofemployee=typeofemployee,
                                             phasetype=phasetype,
                                             noofworkingdays=working_day,
                                             buildstartdate=start_date_year, buildenddate=end_date_year,
                                             runstartdate=start_date_year_run, runenddate=end_date_year_run,
                                             create_timestamp=create_timestamp,
                                             update_timestamp=start_date_year, year=year, quarter=2,
                                             noofresources=noofresources, projid=roleid)
                    LoadPlan_data.save()
                    print(LoadPlan_data)
        except Exception as e:
            print(e)

        context = {
            'noofworkingdays_build': request.session.get('noofworkingdays_build'),
            'noofworkingdays_run': request.session.get('noofworkingdays_run'),
            'noofworkingdays_list': request.session.get('noofworkingdays_list'),
            'role': request.session.get('role'),
        }
        return render(request, 'di_daily_commute.html', context)
    return render(request, 'load_plan.html')


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
    return render(request, 'indirect_impact_el.html')


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



