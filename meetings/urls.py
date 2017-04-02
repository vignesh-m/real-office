from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_meeting'),
    url(r'^create/$', views.create, name='create_meeting'),
    url(r'^list/$', views.view_list, name='list_meeting'),
    url(r'^about/$', views.about, name='about_realoffice'),
    url(r'^success/$', views.success, name='meeting_success'),
    url(r'^view_list/$', views.view_list, name='viewmeeting'),
    url(r'^individual_meeting/$', views.individual_meeting,
        name='individual_meeting'),
]
