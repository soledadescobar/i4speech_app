# -*- coding: utf-8 -*-
import libtmux
from time import gmtime, strftime
import json
from .models import KnownUsers, Instances, InstanceTypes
import requests


# Recibe un DICT y convierte las keys de KEY.subkey a [KEY][SUBKEY]
def convertFormArray(POST, js=False):
    ret = {}
    for k in POST:
        x = k.split('.')
        if len(x) > 1:
            if x[0] not in ret:
                ret[x[0]] = {}
            ret[x[0]][x[1]] = POST[k][-1]
        #else:
            #ret[k] = POST[k]
    if js is True:
        return json.dumps(ret)
    return ret


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


def SaveConfigPost(PST, inst, host):
    POST = PST.copy()
    if '%s.API.user_ids' % str(inst) in POST:
        POST['%s.API.user_ids' % str(inst)] = convertUsers(
            POST['%s.API.user_ids' % str(inst)].split(','),
            '%s' % host,
            'ids')
    for k in list(POST.keys()):
        if k.startswith('%s.' % inst):
            POST['%s' % k.strip("%s." % inst)] = POST.pop(k)
    return convertFormArray(POST, True)


def convertUsers(uids, sv, rt='ids'):
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
            'screen_names': names, 'user_ids': ids}), timeout=5).json()
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


def getInstances():
    return list(Instances.objects.filter(it_id=1).values())


def getInactives():
    return list(Instances.objects.filter(it_id=2).values())