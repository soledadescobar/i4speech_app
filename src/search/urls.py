# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^form/tweets$', views.searchTweets, name='search-tweets'),
    url(r'^search/tweets$', views.search, name='search-tweets-url'),
    url(r'^$', views.index, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)