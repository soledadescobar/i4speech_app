# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from corecontrol.models import Configuration
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import json
from django.contrib.auth.decorators import login_required
from .models import Query, ModelJoin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
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


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
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


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
@csrf_exempt
def get_csv(request, query=None, model=None, join=None, webservice=None):
    if query:
        from .webservices import csv_generator as generator
        from django.db import connections

        q = Query.objects.filter(name=query).get()

        with connections['rest'].cursor() as cursor:
            if request.method == 'POST':
                cursor.execute(q.sql, **request.POST)
            else:
                cursor.execute(q.sql)

            rows = cursor.fetchall()
            description = cursor.description
            params = {
                'keys': [v for v in q.get_params()],
                'values': [v for v in q.get_values()]
            }

            response = StreamingHttpResponse(
                generator(
                    rows,
                    description=description,
                    params=params,
                    headers=True
                ),
                content_type="text/csv"
            )
            response['Content-Disposition'] = 'attachment; filename="%s.csv"' % query
            return response

    elif model and join:
        if model == 'Candidato' and join == 'menciones' and webservice == 'bubblecharts':
            return bubblecharts(request)

        from .models import ModelJoin

        instance = ModelJoin.objects.filter(model=model, name=join, webservice=webservice).all().get()

        import importlib
        mod = getattr(importlib.import_module('control.models'), model)

        if request.method == 'POST':
            raw_rows = mod.objects.filter(**json.loads(request.body)).values(*instance.ws_fields())
        else:
            raw_rows = mod.objects.all().values(*instance.ws_fields())

        from .webservices import csv_join_flare_generator as generator

        response = StreamingHttpResponse(
            generator(
                instance,
                raw_rows
            ),
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % query

        return response


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
@csrf_exempt
def get_json(request, query=None, model=None, filtered=False):
    import json

    if filtered and model and request.method == 'POST':
        import importlib
        from .models import ModelCustomFilter

        custom_filter = ModelCustomFilter.objects.filter(model=model).get()
        fields = custom_filter.fields()
        body = json.loads(request.body)

        mod = getattr(importlib.import_module('control.models'), model)

        for field, method in list(fields.items()):
            if field in body:
                rows = getattr(mod.objects, method)(body.get(field), rest_visible=True).values()

    elif model:
        import importlib
        mod = getattr(importlib.import_module('control.models'), model)

        filters = {}

        if hasattr(mod, 'rest_visible'):
            filters.update({'rest_visible': True})

        if request.method == 'POST':
            filters.update(**json.loads(request.body))
            rows = mod.objects.filter(
                **filters
            ).values(*mod.ws_values())
        else:
            rows = mod.objects.filter(
                **filters
            ).values(*mod.ws_values())

    elif query:
        rows = None

    from .webservices import json_generator as generator

    response = StreamingHttpResponse(
        generator(rows),
        content_type="application/json"
    )

    return response


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
@csrf_exempt
def get_json_cascade(request, model, join, webservice):
    from .models import ModelJoin

    instance = ModelJoin.objects.filter(model=model, name=join, webservice=webservice).all().get()

    import importlib
    mod = getattr(importlib.import_module('control.models'), model)

    if request.method == 'POST':
        raw_rows = mod.objects.filter(
            rest_visible=True,
            **json.loads(request.body)
        ).values('user_id')
    else:
        raw_rows = mod.objects.filter(
            rest_visible=True
        ).values('user_id')

    from .webservices import json_join_cascade_generator as generator

    response = StreamingHttpResponse(
        generator(
            instance,
            raw_rows
        ),
        content_type="application/json"
    )
    response['Content-Disposition'] = 'attachment; filename="%s.json"' % join

    return response


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
@csrf_exempt
def get_tsv(request, query, split=False):
    if split:
        if request.method == 'POST':
            pass
        else:
            pass
    else:
        from .webservices import tsv_generator as generator

        q = Query.objects.filter(name=query).get()

        response = StreamingHttpResponse(
            generator(sql=q.sql),
            content_type="text/tsv"
        )

        return response


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
@csrf_exempt
def get_tsv_actividad(request, frente, split=False):
    import importlib

    Frente = getattr(importlib.import_module('control.models'), 'Frente')
    Candidato = getattr(importlib.import_module('control.models'), 'Candidato')

    ids = tuple(
        c.user_id for c in Candidato.objects.filter(
            frente=Frente.objects.filter(name=frente).get(),
            rest_visible=True
        ).all()
    )

    params = {'ids': ids}

    if split:
        if request.method == 'POST':
            q = Query.objects.filter(name='actividad-filtered').get()
            params.update(**json.loads(request.body))
        else:
            q = Query.objects.filter(name='actividad-splitted').get()

    else:
        q = Query.objects.filter(name='actividad').get()

    from .webservices import tsv_generator as generator

    response = StreamingHttpResponse(
        generator(
            sql=q.sql,
            params=params
        ),
        content_type="text/tsv"
    )

    return response


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def bubblecharts(request):
    import importlib

    Candidato = getattr(importlib.import_module('control.models'), 'Candidato')

    values = ['name', 'screen_name', 'user_id', 'frente__name', 'bloque__name', 'frente__color']

    if request.method == 'POST':
        rows = Candidato.objects.filter(
            rest_visible=True,
            **json.loads(request.body)
        ).values(*values)
    else:
        rows = Candidato.objects.filter(
            rest_visible=True
        ).values(*values)

    from .webservices import bubblecharts_generator as generator

    response = StreamingHttpResponse(
        generator(
            rows
        ),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="bubblecharts.csv"'

    return response


class MentionsMinMax(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)

    permission_classes = (IsAuthenticated, )

    # Modelos Requeridos
    Frente = ('control.models', 'Frente')
    Candidato = ('control.models', 'Candidato')
    UserMention = ('twistreapy.models', 'UserMention')

    # Lista de modelos a importar
    import_models = [
        'Frente',
        'Candidato',
        'UserMention'
    ]

    def get_model(self):
        import importlib

        for mod in self.import_models:
            setattr(
                self, mod, getattr(
                    importlib.import_module(
                        getattr(self, mod)[0]
                    ), getattr(self, mod)[1]
                )
            )

    def get_object(self, name):
        try:
            return self.Candidato.objects.filter(
                frente=self.Frente.objects.get(name=name)
            )

        except self.Frente.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        from .webservices import mentions_min_max as generator
        self.get_model()

        ids = tuple(
            c.user_id for c in self.get_object(name)
        )

        response = StreamingHttpResponse(
            generator(
                ids, self.UserMention
            ),
            content_type="application/json"
        )

        return response


