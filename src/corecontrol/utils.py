# -*- coding: utf-8 -*-
import libtmux
from time import gmtime, strftime
import json
from .models import KnownUsers
import requests


'''# pid = ruta a archivo PID
def prstatus(pid):
    if os.path.exists(pid):
        with open(pid, 'r') as p:
            ppid = int(p.readline())
        if psutil.pid_exists(ppid):
            p = psutil.Process(ppid)
            return datetime.datetime.fromtimestamp(p.create_time()).strftime(
                "%d-%m-%Y %H:%M:%S")
        else:
            return False
    else:
        return False
'''


sv = 'http://localhost:5000'


# inicia el proceso "path" en una nueva session tmux
def startpr(path):
    stoppr(path)
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
'''

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
    return ret'''
'''
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
'''


# Recibe un DICT y convierte las keys de KEY.subkey a [KEY][SUBKEY]
def convertFormArray(POST, js=False):
    ret = {}
    for k in POST:
        x = k.split('.')
        if len(x) > 1:
            if x[0] not in ret:
                ret[x[0]] = {}
            ret[x[0]][x[1]] = POST[k]
        else:
            ret[k] = POST[k]
    if js is True:
        return json.dumps(ret)
    return ret


def readLog(log):
    with open(log, 'r') as lf:
        return lf.read()


def clearLog(log):
    logfile = readLog(log)
    with open(r'/home/gabriel/pst/managecenter/src/logs/%s.log' %
    strftime("%d-%m-%y", gmtime()), 'w') as f:
        f.write(logfile)
    with open(log, 'w'):
        pass
    return True
'''
def getErrors(redis, instance='twistreapy'):
    try:
        queue = Bridge(redis, instance)
        ret = queue.getErrors()
    except Exception as e:
        ret = ['%s' % e]
    return ret
'''


def userLookup(uid=None, scn=None):
    params = {}
    if uid:
        params['user_id'] = uid
    if scn:
        params['screen_name'] = scn
    try:
        q = KnownUsers.objects.get(**params)
    except KnownUsers.DoesNotExist:
        return None
    except KnownUsers.MultipleObjectsReturned:
        return False
    except:
        raise
    else:
        return q


def usersLookup(users):
    ret = []
    for uid in users:
        ret.append({'user_id': uid, 'screen_name':
            userLookup(uid=uid)['screen_name']})


def SaveConfigPost(PST):
    POST = PST.copy()
    if 'API.user_ids' in POST:
        POST['API.user_ids'] = convertUsers(POST['API.user_ids'].split(','),
            'ids')
    return convertFormArray(POST, True)


def convertUsers(uids, rt='ids'):
    ret = []
    names = []
    ids = []
    for uid in uids:
        if uid.startswith('@'):
            look = userLookup(scn=uid[1:])
            if look:
                ret.append(dict(user_id=look['user_id'],
                    screen_name=look['screen_name']))
            else:
                names.append(uid)
        else:
            look = userLookup(uid)
            if look:
                ret.append(dict(user_id=look['user_id'],
                    screen_name=look['screen_name']))
            else:
                ids.append(uid)
    if len(names) > 0 or len(ids) > 0:
        rq = requests.post('%s/get/user_ids' % sv, data=json.dumps({
            'screen_names': names, 'user_ids': ids})).json()
        for key, val in list(rq.items()):
            if not KnownUsers.objects.filter(user_id=key):
                KnownUsers(user_id=key, screen_name=val).save()
            ret.append(dict(user_id=key, screen_name=val))
    if rt == 'ids':
        return returnUsersIds(ret)
    if rt == 'names':
        return returnUsersNames(ret)
    return ret


def returnUsersIds(users):
    ret = []
    for user in users:
        ret.append(str(user['user_id']))
    ret.sort()
    return ",".join(ret)


def returnUsersNames(users):
    ret = []
    for user in users:
        ret.append('@%s' % str(user['screen_name']))
    ret.sort()
    return ",".join(ret)