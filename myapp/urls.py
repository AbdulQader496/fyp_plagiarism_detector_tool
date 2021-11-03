from typing import Pattern
from django.urls import path
from . import views
from myapp import views as myapp_views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('signin.html', views.signin, name='signin'),
    path('index.html', views.index, name='index'),
    path('home.html', views.home, name='home'),
    path('logoutPage.html', views.logout, name='logout'),
    path('fileupload', views.fileupload, name='fileupload'),
    url(r'^fileupload/$', views.fileupload, name='fileupload'),
    ]
