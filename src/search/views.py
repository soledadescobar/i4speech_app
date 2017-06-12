# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from corecontrol.views import make_request
from corecontrol.utils import getInstances
from . import utils


instances = getInstances()


def index(request):
    # Consultar Rates
    ret = {}
    ret['instances'] = {}
    for inst in instances:
        ret['instances'][inst['name']] = make_request(
            request, inst['ip'], 'get/rates/json')
    return render(request, 'search/index.html', ret)


def searchTweets(request):
    return render(request, 'search/search.html')


def search(request):
    #params = utils.searchParams(request.POST)
    ret = utils.procSearch(request.POST)
    return render(request, 'search/search.html', ret)