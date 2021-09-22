from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register',views.register),
    path('login',views.login_user),
    path('logout',views.logout_user),
    path('dashboard',views.dashboard),
    re_path(r'^.*\.html', views.html, name='gentella'),
	path('', views.index, name='index'),
]
