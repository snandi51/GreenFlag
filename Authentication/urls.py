from django.urls import path
from . import views as authentication_views
from Management import views as management_views

urlpatterns = [
    path('', authentication_views.login_user, name='login'),
    path('logout', authentication_views.logout_user, name='logout'),
    path('projectA', management_views.projectA, name='projectA'),
    path('temp', management_views.test_graph, name='temp'),
    path('forgot_password', authentication_views.forgot_password, name='forgot_password'),
    path('change_password', authentication_views.change_password, name='change_password'),
    path('change_password_ok', authentication_views.change_password_ok, name='change_password_ok'),
]