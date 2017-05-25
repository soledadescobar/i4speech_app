# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from corecontrol.views import make_request
from corecontrol.utils import getInstances


instances = getInstances()


# Create your views here.
def index(request, inst=1):
    ret = {}
    ret['inst'] = inst
    instance = [item for item in instances if item['id'] == inst]
    ret.update(make_request(
        request, instance.pop()['ip'], 'get/query/tweet-count'))
    return render(request, 'dashboard/index.html', ret)


def top_hashtags(request, inst=1):
    ret = {}
    ret['inst'] = inst
    instance = [item for item in instances if item['id'] == inst]
    if not len(instance):
        instance.append(instances[0])
    sv = instance.pop()
    ret['top10'] = make_request(
        request, sv['ip'], 'get/json/hashtag-top-20')
    ret['top100'] = make_request(
        request, sv['ip'], 'get/json/hashtag-top-100',
        'json_load')
    return render(request, 'dashboard/top-hashtags.html', ret)


def getTsv(request, inst, query):
    instance = [item for item in instances if item['id'] == inst]
    if not len(instance):
        instance.append(instances[0])
    return HttpResponse(
        make_request(
            request,
            instance.pop()['ip'],
            'get/tsv/%s' % query,
            'content'
        ), content_type="text/tsv"
    )