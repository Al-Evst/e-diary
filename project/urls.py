from django.urls import re_path

from datacenter import views

urlpatterns = [
    re_path(r'^$', views.view_classes, name='classes'),
    re_path(r'^(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)$', views.view_class_info, name='class_info'),
    re_path(r'^(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)/schedule/$', views.view_schedule, name='schedule'),
    re_path(r'^schoolkid/(?P<schoolkid_id>[\w+ ]+)/$', views.view_schoolkid, name='schoolkid'),
    re_path(r'^journal/(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)/(?P<subject_id>[\w+ ]+)/$', views.view_journal, name='journal'),
]