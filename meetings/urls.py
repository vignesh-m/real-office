from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_meeting'),
    url(r'^create/$', views.create, name='create_meeting'),
    url(r'^list/$', views.view_list, name='list_meeting'),
    url(r'^about/$', views.about, name='about_realoffice'),
    url(r'^view_list/$', views.view_list, name='viewmeeting'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^add_room/$', views.add_room, name='add_room'),
    url(r'^search/$', views.search_meeting, name='search'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^report/$', views.report, name='report'),
    url(r'^task_done/$', views.task_done, name='task_done'),
    url(r'^individual_meeting/$', views.individual_meeting,
        name='individual_meeting'),
    url(r'^available_rooms/$', views.available_rooms, name='available_rooms'),
    url(r'^get_notifications/$', views.get_notifications, name='get_notifications'),
    url(r'^report_pdf/$', views.report_pdf, name='report_pdf'),
]
