# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)