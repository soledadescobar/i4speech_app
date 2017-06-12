# -*- coding: utf-8 -*-
import json
import requests
from corecontrol.utils import getInstances


def deleteEmpty(deleteme):
    ret = deleteme.copy()
    for k, v in list(deleteme.items()):
        if v == '':
            del ret[k]
    return ret


def procSearch(params):
    ret = procRequest('search/tweets', json.dumps(params))
    if ret:
        return ret
    ret = {
        'error': True,
        'message': 'Ninguna Instancia Respondió Correctamente',
        'message_type': 'danger',
        'term': params.get('term', ''),
        'raw_query': params.get('raw_query', ''),
        'since': params.get('since', ''),
        'until': params.get('until', ''),
        'since_id': params.get('since_id', ''),
        'max_id': params.get('max_id', '')
        }
    return deleteEmpty(ret)


def procTimeline(params):
    ret = procRequest('search/timeline', json.dumps(params))
    if ret:
        return ret
    ret = {
        'error': True,
        'message': 'Ninguna Instancia Respondió Correctamente',
        'message_type': 'danger',
        'user_id': params.get('user_id', ''),
        'screen_name': params.get('screen_name', ''),
        'since_id': params.get('since_id', ''),
        'max_id': params.get('max_id', '')
        }
    return deleteEmpty(ret)


def procRetweets(params):
    ret = procRequest('search/retweets', json.dumps(params))
    if ret:
        return ret
    ret = {
        'error': True,
        'message': 'Ninguna Instancia Respondió Correctamente',
        'message_type': 'danger',
        'tweet_id': params.get('tweet_id', ''),
        }
    return deleteEmpty(ret)


def procFfs(params):
    ret = procRequest('search/ffs', json.dumps(params))
    if ret:
        return ret
    ret = {
        'error': True,
        'message': 'Ninguna Instancia Respondió Correctamente',
        'message_type': 'danger',
        'user_id': params.get('user_id', ''),
        }
    return deleteEmpty(ret)


def procRequest(url, dat, t=15):
    instances = getInstances()
    for i in instances:
        try:
            r = requests.post(
                '%s/%s' % (i['ip'], url),
                data=dat,
                timeout=t)
        except:
            continue
        if r.status_code == requests.codes.ok:
            rq = r.json()
            if rq.get('error', False):
                continue
            return rq
    return False