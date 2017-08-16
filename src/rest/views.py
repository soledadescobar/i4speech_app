# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from corecontrol.models import Configuration
from django.http import HttpResponse
from functools import wraps
import json
from django.contrib.auth.decorators import login_required
# Create your views here.


def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                username, password = auth.split(':', 1)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
        return func(request, *args, **kwargs)
    return _decorator


@http_basic_auth
@login_required
def get_server_configuration(request, pk):
    config = Configuration.objects.filter(server=pk).get()

    response = {
        'track': [],
        'follow': []
    }

    for keyword in config.keywords.all():
        response['track'].append(keyword.name)

    for candidato in config.candidatos.all():
        response['follow'].append(candidato.screen_name)

    return HttpResponse(json.dumps(response), content_type='application/json')
