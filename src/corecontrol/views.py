# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse

from .utils import *

ini = r'/home/gabriel/pst/twistreapy/src/config.ini'
pid = r'/tmp/twistreapy.pid'
svc = r'/home/gabriel/pst/twistreapy/src/'


# Create your views here.
def index(request):
    ret = {}
    ret['running'] = prstatus(pid)
    ret['pidfile'] = pid
    ret['inifile'] = ini
    ret['svcpath'] = svc
    return render(request, 'corecontrol/index.html', ret)


def config(request, ret={}):
    cfg = getconfig(ini)
    ret['API'] = cfg['API']
    ret['DATABASE'] = cfg['DATABASE']
    ret['inifile'] = ini
    return render(request, 'corecontrol/config.html', ret)


def saveconfig(request):
    savecfg(ini, convertFormArray(request.POST))
    #return JsonResponse((request.POST))
    if(request.POST['action'] == 'saverestart'):
        stoppr(pid)
        startpr(svc)
    return config(request, ret={'message': 'Configuración Guardada'})


def startproc(request):
    ret = {}
    if prstatus(pid):
        ret['error'] = True
        ret['running'] = True
        ret['message'] = 'El servicio ya se esta ejecutando'
    else:
        startpr(svc)
        if prstatus(pid):
            ret['error'] = False
            ret['running'] = True
            ret['message'] = 'ok_server_running'
        else:
            ret['error'] = True
            ret['running'] = False
            ret['message'] = 'error_starting_server'
    return JsonResponse(ret)


def stopproc(request):
    ret = {}
    if stoppr(pid):
        ret['error'] = False
        ret['message'] = 'Servicio Detenido Exitosamente'
    else:
        ret['error'] = True
        ret['message'] = 'No se pudo detener el Servicio'
    return JsonResponse(ret)