# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^config/(?P<view>\w+)/save/instance-(?P<inst>\d+)', views.saveconfig),
    url(r'^config/(?P<view>\w+)', views.config),
    url(r'^config', views.config, name='config'),
    url(r'^service/start/instance-(?P<inst>\d+)', views.startproc),
    url(r'^service/start', views.startproc, name='startproc'),
    url(r'^service/stop/instance-(?P<inst>\d+)', views.stopproc),
    url(r'^service/stop', views.stopproc, name='stopproc'),
    url(r'^service/clearlog/instance-(?P<inst>\d+)',
        views.clearlog, name='clearlog'),
    url(r'^service/redis/start', views.startrd, name='startrd'),
    url(r'^services', views.services, name='services'),
    url(r'^status', views.status, name='status'),
    url(r'^log/instance-(?P<inst>\d+)/download',
        views.downloadlog, name='logdl'),
    url(r'^log/instance-(?P<inst>\d+)', views.logfile),
    url(r'^log', views.logfile, name='log'),
    url(r'^tmp-cfg/$', views.ConfigurationsListView.as_view(), name='configuration'),
    url(r'^$', views.status, name='corecontrol'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)