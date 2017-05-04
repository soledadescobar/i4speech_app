# -*- coding: utf-8 -*-
import psutil
import os.path
import configparser
import libtmux


# pid = ruta a archivo PID
def prstatus(pid):
    if os.path.exists(pid):
        with open(pid, 'r') as p:
            ppid = int(p.readline())
        if psutil.pid_exists(ppid):
            p = psutil.Process(ppid)
            return p.is_running()
        else:
            return False
    else:
        return False


# inicia el proceso "path" en una nueva session tmux
def startpr(path):
    tmux = libtmux.Server()
    tmux.remove_environment('PATH')
    tmux.remove_environment('VIRTUAL_ENV')
    session = tmux.new_session('twistreapy', True, False, path)
    pane = session.attached_pane
    pane.send_keys('source ../venv/bin/activate')
    pane.send_keys('python __main__.py start')
    return True


def stoppr(path):
    tmux = libtmux.Server()
    if tmux.has_session('twistreapy'):
        tmux.kill_session('twistreapy')
        return True
    return False


# ini = ruta a archivo config.ini
def getconfig(ini):
    cp = configparser.ConfigParser()
    cp.read(ini)
    apicfg = cp['API']
    dbcfg = cp['DATABASE']
    ret = {'API': {}, 'DATABASE': {}}
    for t in list(apicfg.items()):
        # Fix: Convierte a listas los campos especificos separados por coma
        if t[0] == 'keywords' or t[0] == 'user_ids' or t[0] == 'entities':
            ret['API'][t[0]] = ",".join(t[1].split(','))
        else:
            ret['API'][t[0]] = t[1]
    for t in list(dbcfg.items()):
        ret['DATABASE'][t[0]] = t[1]
    return ret


def savecfg(ini, POST):
    ## Remove action y token del post
    if 'csrfmiddlewaretoken' in POST:
        del POST['csrfmiddlewaretoken']
    if 'action' in POST:
        del POST['action']
    cp = configparser.ConfigParser()
    cp.read(ini)
    for t, c in list(POST.items()):
        y = dict(c)
        for k, v in list(y.items()):
            cp.set(t, k, v)
    with open(ini, 'wb') as cfile:
        cp.write(cfile)
    #TODO: Tratar excepciones
    return True


# Recibe un DICT y convierte las keys de KEY.subkey a [KEY][SUBKEY]
def convertFormArray(POST):
    ret = {}
    for k in POST:
        x = k.split('.')
        if len(x) > 1:
            if x[0] not in ret:
                ret[x[0]] = {}
            ret[x[0]][x[1]] = POST[k]
        else:
            ret[k] = POST[k]
    return ret
