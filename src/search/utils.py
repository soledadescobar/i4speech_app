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
    instances = getInstances()
    dat = json.dumps(params)
    for i in instances:
        #TODO: Tratar timoutes en este post
        try:
            r = requests.post(
                '%s/search/tweets' % i['ip'],
                data=dat,
                timeout=15)
        except:
            continue
        if r.status_code == requests.codes.ok:
            rq = r.json()
            if rq.get('error', False):
                continue
            return rq
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