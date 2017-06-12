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
    url(r'^tweets$', views.search, name='search-tweets-url'),
    url(r'^timeline$', views.timeline, name='search-timeline-url'),
    url(r'^retweets$', views.searchRetweets, name='search-retweets-url'),
    url(r'^ffs$', views.searchFfs, name='search-ffs-url'),
    url(r'^$', views.index, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)