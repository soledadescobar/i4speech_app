# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from corecontrol.views import make_request


sv = 'http://localhost:5000'


# Create your views here.
def index(request):
    ret = {}
    ret['tweets'] = make_request(request, sv, 'get/query/tweet-count')
    ret['tweetsday'] = make_request(request, sv, 'get/tsv/tweet-count-day',
        'content')
    ret['hashtags'] = make_request(request, sv, 'get/query/hashtag-count')
    return render(request, 'dashboard/index.html', ret)