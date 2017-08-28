# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from corecontrol.models import Configuration
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import json
from django.contrib.auth.decorators import login_required
from .models import Query, ModelJoin
# Create your views here.


class Echo(object):
    def write(self, value):
        return value


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
def get_server_configuration(request, name):
    config = Configuration.objects.filter(server__name=name).get()

    response = {
        'track': [],
        'follow': [],
        'apikey': {}
    }

    for keyword in config.keywords.all():
        response['track'].append(keyword.name)

    for candidato in config.candidatos.all():
        response['track'].append("@%s" % candidato.screen_name)
        if candidato.user_id:
            response['follow'].append(str(candidato.user_id))

    response['apikey'] = config.server.get_apikeys()

    return HttpResponse(json.dumps(response), content_type='application/json')


@http_basic_auth
@login_required
@csrf_exempt
def get_csv(request, query=None, model=None, join=None):
    from .webservices import csv_generator

    if query:
        from django.db import connections

        q = Query.objects.filter(name=query).get()

        with connections['rest'].cursor() as cursor:
            if request.method == 'POST':
                cursor.execute(q.sql, **request.POST)
            else:
                cursor.execute(q.sql)

            rows = cursor.fetchall()
            description = cursor.description

    elif model:
        import importlib
        mod = getattr(importlib.import_module('control.models'), model)

        if request.method == 'POST':
            raw_rows = mod.objects.filter(**json.loads(request.body)).values(*mod.ws_values())
        else:
            raw_rows = mod.objects.all().values(*mod.ws_values(extra=True))

        if join:
            j = ModelJoin.objects.filter(model=model, name=join).all().get()

            from django.db import connections

            with connections['rest'].cursor() as cursor:
                params = j.ws_fields
                for k, v in list(params.items()):
                    params[k] = (i.get(v) for i in raw_rows)

                params = {'ids': (138814032, 24900072, 3343144691)}
                cursor.execute(j.sql, **params)

                print(cursor)
                return cursor

    response = StreamingHttpResponse(
        csv_generator(
            rows,
            description=description,
            params={
                'keys': [v for v in q.get_params()],
                'values': [v for v in q.get_values()]
            },
            headers=True
        ),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % query
    return response


@http_basic_auth
@login_required
@csrf_exempt
def get_json(request, query=None, model=None):
    from .webservices import json_generator
    import json

    if model:
        import importlib
        mod = getattr(importlib.import_module('control.models'), model)
        if request.method == 'POST':
            rows = mod.objects.filter(**json.loads(request.body)).values(*mod.ws_values())
        else:
            rows = mod.objects.all().values(*mod.ws_values())
    elif query:
        pass

    response = StreamingHttpResponse(
        json_generator(rows),
        content_type="application/json"
    )

    return response
