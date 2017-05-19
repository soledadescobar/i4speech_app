# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from .utils import *


ini = r'/home/abottiggi/twistreapy/src/config.ini'
pid = r'/tmp/twistreapy.pid'
pipe = r'/tmp/twistreapy.pip'
svc = r'/home/abottiggi/twistreapy/src/'
lgf = r'/home/abottiggi/twistreapy/src/output.log'
redis = {'host': 'localhost', 'port': 6379, 'decode_responses': True}
sv = 'http://10.128.0.6:5000'
#sv = 'http://localhost:5000'


# Create your views here.
def status(request, ret={}):
    # Consultar Status
    #ret.update(requests.get('%s/get/status' % sv).json())
    ret.update(make_request(request, sv, 'get/status'))
    ret['pidfile'] = pid
    ret['inifile'] = ini
    ret['svcpath'] = svc
    #ret['rderrors'] = getErrors(redis)
    return render(request, 'corecontrol/status.html', ret)


def config(request, ret={}, view='api'):
    #cfg = getconfig(ini)
    cfg = make_request(request, sv, 'get/config.ini')
    ret['view'] = view
    ret[view.upper()] = cfg[view.upper()]
    if view == 'api':
        kws = ret['API']['keywords'].split(',')
        kws.sort()
        ret['API']['keywords'] = ",".join(kws)
        ret['API']['user_ids'] = convertUsers(ret['API']['user_ids'].split(','),
             'names')
    ret['inifile'] = ini
    return render(request, 'corecontrol/config-%s.html' % view, ret)


def configdb(request, ret={}):
    cfg = make_request(request, sv, 'get/config.ini')
    ret['API'] = cfg['API']
    ret['DATABASE'] = cfg['DATABASE']
    ret['inifile'] = ini
    return render(request, 'corecontrol/config-database.html', ret)


def saveconfig(request, view='api'):
    dat = SaveConfigPost(request.POST)
    rq = requests.post('%s/save/config.ini' % sv,
        data=dat).json()
    # savecfg(ini, convertFormArray(request.POST))
    if(request.POST['action'] == 'saverestart'):
        make_request(request, sv, 'service/twistreapy/start')
    return config(request,
        ret=rq,
        view=view
    )


def startproc(request, ret={}):
    make_request(request, sv, 'service/twistreapy/start')
    ret.update(make_request(request, sv, 'get/status'))
    if ret['running']:
        ret['message_type'] = 'success'
        ret['message'] = 'Servicio Iniciado Exitosamente'
    else:
        ret['message_type'] = 'danger'
        ret['message'] = 'El Servicio no se Inicio Correctamente'
    return status(request, ret)


def stopproc(request, ret={}):
    make_request(request, sv, 'service/twistreapy/stop')
    ret.update(make_request(request, sv, 'get/status'))
    ret['message_type'] = 'info'
    ret['message'] = 'Servicio Detenido'
    return status(request, ret)


def logfile(request, ret={}, raw=False):
    ret['output'] = make_request(request, sv, 'get/log', 'content')
    if raw:
        return HttpResponse(ret['output'], content_type='text/plain')
    else:
        return render(request, 'corecontrol/log.html', ret)


def clearlog(request, ret={}):
    make_request(request, sv, 'clear/log')
    ret['message'] = 'LOG Archivado y Limpiado Exitosamente'
    ret['message_type'] = 'success'
    return logfile(request, ret)


def startrd(request, ret={}):
    make_request(request, sv, 'service/redis/start')
    ret.update(make_request(request, sv, 'get/status'))
    if ret['redis']:
        ret['message_type'] = 'success'
        ret['message'] = 'Redis Iniciado Correctamente'
    else:
        ret['message_type'] = 'danger'
        ret['message'] = 'No se pudo iniciar el servidor Redis'
    return status(request, ret)


def downloadlog(request):
    return logfile(request, raw=True)


def services(request):
    pass


def make_request(request, host, url, ret='json'):
    try:
        rq = requests.get('%s/%s' % (host, url))
    except:
        return render(request, 'corecontrol/connection-error.html')
    if ret == 'json':
        return rq.json()
    if ret == 'json_load':
        return json.loads(rq.json())
    elif ret == 'content':
        return rq.content
    elif ret == 'text':
        return rq.text
    else:
        return rq.json()
