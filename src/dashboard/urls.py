# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^instance-(?P<inst>[0-9]+)/(?P<query>[a-zA-Z0-9_-]+).tsv$',
        views.getTsv),
    url(r'^top-hashtags$', views.top_hashtags, name='tophtgs'),
    url(r'^$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)