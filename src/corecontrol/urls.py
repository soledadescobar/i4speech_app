# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^config/save', views.saveconfig, name='saveconfig'),
    url(r'^config', views.config, name='config'),
    url(r'^startproc', views.startproc, name='startproc'),
    url(r'^stopproc', views.stopproc, name='stopproc'),
    url(r'^$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)