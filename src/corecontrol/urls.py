# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.ConfigurationsListView.as_view(), name='index'),
    url(r'^servers/$', views.ServersListView.as_view(), name='servers'),
    url(r'^servers/config$', views.ConfigurationsListView.as_view(), name='servers-config'),
    url(r'^server-(?P<pk>[0-9]*)/status$', views.get_server_status, name='server-status'),
    url(r'^server-(?P<pk>[0-9]*)/restart', views.get_server_status, name='server-restart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
