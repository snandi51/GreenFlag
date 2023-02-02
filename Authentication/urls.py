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
    path('Help', management_views.Help, name='Help'),
    path('temp', management_views.test_graph, name='temp'),
    path('forgot_password', authentication_views.forgot_password, name='forgot_password'),
    path('index', management_views.index, name='index'),
    path('change_password', authentication_views.change_password, name='change_password'),
    path('change_password_ok', authentication_views.change_password_ok, name='change_password_ok'),
]

handler400 = "Management.views.error_400"
handler403 = "Management.views.error_403"
handler404 = "Management.views.error_404"
handler500 = "Management.views.error_500"
