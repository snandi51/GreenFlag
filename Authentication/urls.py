from django.urls import path
from . import views as authentication_views

urlpatterns = [
    path('', authentication_views.login_user, name='login'),
    path('logout', authentication_views.logout_user, name='logout'),

]