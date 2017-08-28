# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# from corecontrol.views import make_request
# from corecontrol.utils import getInstances
from . import utils, tasks


def index(request):
    # Consultar Rates
    task = tasks.tweet_search()
    print(task)
    ret = {}
    return render(request, 'search/index.html', ret)


def searchTweets(request):
    return render(request, 'search/search.html')


def search(request):
    ret = utils.procSearch(request.POST)
    return render(request, 'search/search.html', ret)


def searchTimeline(request):
    return render(request, 'search/timeline.html')


def timeline(request):
    ret = utils.procTimeline(request.POST)
    return render(request, 'search/timeline.html', ret)


def retweets(request):
    return render(request, 'search/retweets.html')


def searchRetweets(request):
    ret = utils.procRetweets(request.POST)
    return render(request, 'search/retweets.html', ret)


def ffs(request):
    return render(request, 'search/ffs.html')


def searchFfs(request):
    ret = utils.procFfs(request.POST)
    return render(request, 'search/ffs.html', ret)