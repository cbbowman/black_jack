from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^.*\.html', views.html, name='gentella'),
	path('', views.index, name='index'), 
	]