from django.urls import path
from . import views as authentication_views
from Management import views as management_views

urlpatterns = [
    path('', authentication_views.login_user, name='login'),
    path('logout', authentication_views.logout_user, name='logout'),
    path('projectA', management_views.projectA, name='projectA'),
    path('forget_password', authentication_views.forget_password, name='forget_password'),
    path('change_password', authentication_views.change_password, name='change_password'),
    path('change_password_ok', authentication_views.change_password_ok, name='change_password_ok'),
]