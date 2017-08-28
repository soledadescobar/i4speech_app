# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    url(r'^candidatos$', CandidatosListView.as_view(), name='candidatos'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
