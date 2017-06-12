# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^form/tweets$', views.searchTweets, name='search-tweets'),
    url(r'^form/timeline$', views.searchTimeline, name='search-timeline'),
    url(r'^form/retweets$', views.retweets, name='search-retweets'),
    url(r'^form/ffs$', views.ffs, name='search-ffs'),
    url(r'^search/tweets$', views.search, name='search-tweets-url'),
    url(r'^search/timeline$', views.timeline, name='search-timeline-url'),
    url(r'^search/retweets$', views.searchRetweets, name='search-retweets-url'),
    url(r'^search/ffs$', views.searchFfs, name='search-ffs-url'),
    url(r'^$', views.index, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)