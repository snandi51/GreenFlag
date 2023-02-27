from django.urls import path
from . import views as authentication_views
from Management import views as management_views

urlpatterns = [
    path('', authentication_views.login_user, name='login'),
    path('logout', authentication_views.logout_user, name='logout'),
    path('400', management_views.error_400, name='400'),
    path('403', management_views.error_403, name='403'),
    path('404', management_views.error_404, name='404'),
    path('500', management_views.error_500, name='500'),
    path('projectA', management_views.projectA, name='projectA'),
    path('company_detail', management_views.company_detail, name='company_detail'),
    path('Indirect_Impact', management_views.Indirect_Impact, name='Indirect_Impact'),
    path('indirect_impact_mc', management_views.indirect_impact_mc, name='indirect_impact_mc'),
    path('di_business_travel', management_views.di_business_travel, name='di_business_travel'),
    path('di_daily_commute', management_views.di_daily_commute, name='di_daily_commute'),
    path('di_monitor', management_views.di_monitor, name='di_monitor'),
    path('di_drone', management_views.di_drone, name='di_drone'),
    path('di_laptop', management_views.di_laptop, name='di_laptop'),
    path('di_dcn', management_views.di_dcn, name='di_dcn'),
    path('di_pc', management_views.di_pc, name='di_pc'),
    path('di_tablet', management_views.di_tablet, name='di_tablet'),  
    path('di_telephone', management_views.di_telephone, name='di_telephone'),
    path('di_printer', management_views.di_printer, name='di_printer'),
    path('di_bt_speaker', management_views.di_bt_speaker, name='di_bt_speaker'),
    path('di_projector', management_views.di_projector, name='di_projector'),
    path('di_camera', management_views.di_camera, name='di_camera'),
    path('di_camera', management_views.di_camera, name='di_camera'),
    path('di_connected_sensor', management_views.di_connected_sensor, name='di_connected_sensor'),
    path('di_lidar', management_views.di_lidar, name='di_lidar'),
    path('di_raspberrypi', management_views.di_raspberrypi, name='di_raspberrypi'),
    path('load_plan', management_views.load_plan, name='load_plan'),
    path('di_daily_commute', management_views.di_daily_commute, name='di_daily_commute'),
    path('Help', management_views.Help, name='Help'),
    path('emission_lib', management_views.emission_lib, name='emission_lib'),
    path('datacenter_network', management_views.datacenter_network, name='datacenter_network'),
    path('indirect_impact_el', management_views.indirect_impact_el, name='indirect_impact_el'),
    path('indirect_impact_fl', management_views.indirect_impact_fl, name='indirect_impact_fl'),
    path('indirect_impact_wt', management_views.indirect_impact_wt, name='indirect_impact_wt'),
    path('indirect_impact_waste', management_views.indirect_impact_waste, name='indirect_impact_waste'),
    path('indirect_impact_rm', management_views.indirect_impact_rm, name='indirect_impact_rm'),
    path('indirect_impact_plastic', management_views.indirect_impact_plastic, name='indirect_impact_plastic'),
    path('indirect_impact_paper', management_views.indirect_impact_paper, name='indirect_impact_paper'),
    path('temp', management_views.test_graph, name='temp'),
    path('forgot_password', authentication_views.forgot_password, name='forgot_password'),
    path('index', management_views.index, name='index'),
    path('change_password', authentication_views.change_password, name='change_password'),
    path('change_password_ok', authentication_views.change_password_ok, name='change_password_ok'),
    path('detailed_view_cmo', management_views.detailed_view_cmo, name='detailed_view_cmo'),
    path('view_detailed_result', management_views.view_detailed_result, name='view_detailed_result'),
]

handler400 = "Management.views.error_400"
handler403 = "Management.views.error_403"
handler404 = "Management.views.error_404"
handler500 = "Management.views.error_500"
