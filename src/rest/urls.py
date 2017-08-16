# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    url(r'^get/server-(?P<pk>[0-9]*)/config$', get_server_configuration),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
