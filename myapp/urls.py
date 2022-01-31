from typing import Pattern
from django.urls import path
from . import views
from myapp import views as myapp_views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.landing_page),
    path('index.html', views.index, name='index'),
    path('signin.html', views.signin, name='signin'),
    path('index.html', views.index, name='index'),
    path('home.html', views.home, name='home'),
    path('signin.html', views.logout, name='logout'),
    path('fileupload', views.fileupload, name='fileupload'),
    #path('report.html', views.fileupload, name='fileupload1'),
    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),
    path('delete_class/<int:id>/', views.delete_class, name='delete_class'),
    path('delete_class_file/<int:id>/', views.delete_class_file, name='delete_class_file'),
    path('report.html', views.returnTableWithURL, name='returnTableWithURL'),
    # path('reportREP.html', views.returnTableWithURL2, name='returnTableWithURL2'),
    path('classDiv', views.classDiv, name='classDiv'),
    path('class_fileupload', views.class_fileupload, name='class_fileupload'),
    path('submit.html', views.class_fileupload, name='class_fileupload'),
    path('reportrep.html', views.class_file_upload_confirmation,name='class_file_upload_confirmation'),
    #path('success.html', views.class_fileupload, name='class_fileupload')
    #path('unsuccesful.html', views.class_fileupload, name='class_fileupload'),
    path('classFileUpload', views.class_file_upload_view, name='class_file_upload_view'),
    path('<uuid>',  views.class_file_upload_view, name='class_file_upload_view'),
    # path('report.html', views.fileupload, name='report'),,
    ]
