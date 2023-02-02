from django.shortcuts import render
import django
from MyProjects.models import ProjectDetails

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


def projectA(request):
    """
    Project Duration
    Project Details
    Project Roles
    Direct Impact Parameters
    Indirect Impact Parameters
    """
    if request.method == 'POST':
        start_date_build = request.POST.get('start_date_build')
        end_date_build = request.POST.get('start_date_build')
        start_date_run = request.POST.get('start_date_run')
        end_date_run = request.POST.get('end_date_run')

        pl_1 = request.POST.get('pl_1')
        ps = request.POST.get('ps')
        bu = request.POST.get('bu')
        department = request.POST.get('department')
        development = request.POST.get('development')
        type_project = request.POST.get('type_project')

        name = request.POST.get('name')
        work_country = request.POST.get('work_country')

        pro_manager = request.POST.get('pro_manager')
        proxy = request.POST.get('proxy')
        data = request.POST.get('data')
        it_1 = request.POST.get('it_1')
        it_2 = request.POST.get('it_2')
        it_front = request.POST.get('it_front')
        director = request.POST.get('director')
        project = request.POST.get('project')

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

        # ProjId = request.user.id

        # fuel = request.POST.get('fuel')
        # electricity = request.POST.get('electricity')
        # water = request.POST.get('water')
        # paper = request.POST.get('paper')
        # plastic = request.POST.get('plastic')
        # waste_material = request.POST.get('waste_material')
        # raw_material = request.POST.get('raw_material')
        # import ipdb
        # ipdb.set_trace()
        ProjectDetails_db = ProjectDetails.objects.all()
        print(ProjectDetails_db)
        Year = 2022
        Quarter = 2

        project_details_data = ProjectDetails(projectname=name, projectlocation=pl_1,
                                               department=department,
                                               whichuserequipment=WhichUserEquipment,
                                               whichindustrialequipment=WhichIndustrialEquipment,
                                               whichparametersimplemented=WhichParametersImplemented,
                                               buconcerned=bu, projectstatus=ps, phasetype=type_project,
                                               buildstartdate=start_date_build, buildenddate=end_date_build,
                                               runstartdate=start_date_run, runenddate=end_date_run,
                                               year=Year, quarter=Quarter, create_timestamp=start_date_build,
                                               update_timestamp=start_date_build)
        project_details_data.save()
        print(project_details_data)

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
            'pro_manager': pro_manager,
            'proxy': proxy,
            'data': data,
            'it_1': it_1,
            'it_2': it_2,
            'it_front': it_front,
            'director': director,
            'project': project,
            'WhichUserEquipment': WhichUserEquipment,
            'WhichIndustrialEquipment': WhichIndustrialEquipment,
            'WhichParametersImplemented': WhichParametersImplemented,
            'development': development,
            # 'laptop': laptop,
            # 'pc': pc,
            # 'tablet': tablet,
            # 'telephone': telephone,
            # 'printer': printer,
            # 'speaker': speaker,
            # 'projector': projector,
            # 'monitor': monitor,
            # 'laptop1': laptop1,
            # 'camera': camera,
            # 'sensor': sensor,
            # 'lidar': lidar,
            # 'fuel': fuel,
            # 'electricity': electricity,
            # 'water': water,
            # 'paper': paper,
            # 'plastic': plastic,
            # 'waste_material': waste_material,
            # 'raw_material': raw_material,
        }
        return render(request, 'projectA.html', context)
    return render(request, 'projectA.html')


def company_detail(request):
    return render(request, 'company_detail.html')


def Help(request):
    return render(request, 'Help.html')


def Indirect_Impact(request):
    return render(request, 'Indirect_Impact.html')


def test_graph(request):
    return render(request, 'temp.html')


def error_400(request, exception):
    return render(request, '400.html')


def error_403(request, exception):
    return render(request, '403.html')


def error_404(request, exception):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')



