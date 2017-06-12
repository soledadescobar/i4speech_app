# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from corecontrol.views import make_request
from corecontrol.utils import getInstances
from . import utils


def index(request):
    # Consultar Rates
    ret = {}
    ret['instances'] = {}
    instances = getInstances()
    for inst in instances:
        ret['instances'][inst['name']] = make_request(
            '', inst['ip'], 'get/rates/json')
    return render(request, 'search/index.html', ret)


def searchTweets(request):
    return render(request, 'search/search.html')


def search(request):
    #params = utils.searchParams(request.POST)
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