# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from corecontrol.views import make_request


sv = 'http://10.128.0.6:5000'
#sv = 'http://localhost:5000'


# Create your views here.
def index(request):
    ret = {}
    ret.update(make_request(request, sv, 'get/query/tweet-count'))
    return render(request, 'dashboard/index.html', ret)


def top_hashtags(request):
    ret = {}
    ret['top10'] = make_request(request, sv, 'get/json/hashtag-top-20')
    ret['top100'] = make_request(request, sv, 'get/json/hashtag-top-100',
        'json_load')
    return render(request, 'dashboard/top-hashtags.html', ret)


def getTsv(request, query):
    return HttpResponse(
        make_request(
            request,
            sv,
            'get/tsv/%s' % query,
            'content'
        ), content_type="text/tsv"
    )