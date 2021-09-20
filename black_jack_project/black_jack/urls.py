from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    path('register',views.register),
    path('login',views.login_user),
    path('logout',views.logout_user),
]

if settings.DEBUG:
    urlpatterns.extend([
        path('test', views.test_page),
        path('test/display', views.test_display),
        path('test/reset', views.test_reset),
        path('test/new_game', views.test_new_game),
        path('test/hit', views.test_hit),
        path('test/stand', views.test_stand),
        path('test/double_down', views.test_double_down),
        path('test/split', views.test_split),
        path('test/insurance', views.test_take_insurance),
        path('test/setup_game', views.test_setup_game),
    ])