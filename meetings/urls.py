from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_meeting'),
    url(r'^create/$', views.create, name='create_meeting'),
    url(r'^list/$', views.view_list, name='list_meeting'),
    url(r'^about/$', views.about, name='about_realoffice'),
    url(r'^view_list/$', views.view_list, name='viewmeeting'),
]
