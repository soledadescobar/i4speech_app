# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from .utils import *


instances = getInstances()


# Create your views here.
def status(request, ret={}):
    # Consultar Status
    ret['instances'] = []
    for i in instances:
        ret['instances'].append(
            {"id": i['id'],
            "output": make_request(request, '%s' % i['ip'], 'get/status')})
        ret['instances'][-1].update(i)
    return render(request, 'corecontrol/status.html', ret)


def config(request, ret={}, view='api', inst=False):
    ret['instances'] = instances
    ret['view'] = view
    for i, val in enumerate(ret['instances']):
        ret['instances'][i].update(
            make_request(
                request,
                '%s' % val['ip'],
                'get/config.ini'))
        if ret['instances'][i].get('timeout', False):
            continue
        kws = ret['instances'][i]['API']['keywords'].split(',')
        kws.sort()
        ret['instances'][i]['API']['keywords'] = ",".join(kws)
        ret['instances'][i]['API']['user_ids'] = convertUsers(
            ret['instances'][i]['API']['user_ids'].split(','), 'names')
    if inst:
        ret['anchor'] = 'instances-%s' % inst
    return render(request, 'corecontrol/config.html', ret)


def saveconfig(request, inst, view='api', ret={}):
    item = None
    for i in instances:
        if int(i.get('id', False)) == int(inst):
            item = i
    #instance = next((item for item in instances if item['id'] == inst))
    #instance =
    #[item for item in instances if str(item['id']) == str(inst)]
    #[item['id'] for item in instances if item['id'] == inst]
    dat = SaveConfigPost(request.POST, inst, item['ip'])
    rq = requests.post('%s/save/config.ini' % item['ip'],
        data=dat).json()
    # savecfg(ini, convertFormArray(request.POST))
    if(request.POST.get('action', False) == 'saverestart'):
        make_request(request, item['ip'], 'service/twistreapy/start')
    return config(request,
        ret=rq,
        view=view,
        inst=inst
    )


def startproc(request, inst, ret={}):
    instance = [item for item in instances if item['id'] == inst]
    sv = instance.pop()
    make_request(request, sv['ip'], 'service/twistreapy/start')
    ret.update(make_request(request, sv['ip'], 'get/status'))
    if ret['running']:
        ret['message_type'] = 'success'
        ret['message'] = 'Servicio Iniciado Exitosamente'
    else:
        ret['message_type'] = 'danger'
        ret['message'] = 'El Servicio no se Inicio Correctamente'
    return status(request, ret)


def stopproc(request, inst, ret={}):
    instance = [item for item in instances if item['id'] == inst]
    sv = instance.pop()
    make_request(request, sv['ip'], 'service/twistreapy/stop')
    ret.update(make_request(request, sv['ip'], 'get/status'))
    ret['message_type'] = 'info'
    ret['message'] = 'Servicio Detenido'
    return status(request, ret)


def logfile(request, inst=False, ret={}, raw=False):
    ret['instances'] = []
    for i in instances:
        ret['instances'].append(
            make_request(
                request,
                instance['ip'],
                'get/log',
                'content'))
    if raw:
        return HttpResponse(ret, content_type='text/plain')
    else:
        if inst:
            ret['anchor'] = 'instances-%s' % inst
        return render(request, 'corecontrol/log.html', ret)


def clearlog(request, inst, ret={}):
    instance = [item for item in instances if item['id'] == inst]
    make_request(request, instance['ip'], 'clear/log')
    ret['message'] = 'LOG Archivado y Limpiado Exitosamente'
    ret['message_type'] = 'success'
    return logfile(request, ret)


def startrd(request, ret={}):
    instance = [item for item in instances if item['id'] == inst]
    make_request(request, instance['ip'], 'service/redis/start')
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
        rq = requests.get('%s/%s' % (host, url), timeout=5)
    except:
        return {'timeout': True}
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
