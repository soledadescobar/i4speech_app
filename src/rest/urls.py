# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    url(r'^get/server/(?P<name>[a-zA-Z0-9-]*)/config$', get_server_configuration),
    url(r'^get/csv/query/(?P<query>[a-zA-Z0-9-_]*)/$', get_csv),
    url(r'^get/csv/model/(?P<model>[a-zA-Z0-9-_]*)/(?P<join>[a-zA-Z]*)/(?P<webservice>[a-zA-Z0-9-_]*)/$', get_csv),
    url(r'^get/json/query/(?P<query>[a-zA-Z0-9-_]*)/$', get_json),
    url(r'^get/json/model/(?P<model>[a-zA-Z0-9-_]*)/$', get_json),
    url(r'^get/json/filter/(?P<model>[a-zA-Z0-9-_]*)/$', get_json, {'filtered': True}),
    url(r'^get/tsv/query/(?P<query>[a-zA-Z0-9-_]*)/$', get_tsv),
    url(r'^get/tsv/actividad/(?P<frente>[a-zA-Z0-9-_ ]*)/$', get_tsv_actividad),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
