# -*- coding: utf-8 -*-
import redis
#import json


class Bridge(object):
    rediss = ''
    instance = ''
    queue = ''
    errors = ''

    def __init__(self, redisc, instance, queue='QUEUE', errors='ERRORS'):
        self.rediss = redis.Redis(**redisc)
        self.instance = instance
        self.queue = '%s-%s' % (queue, instance)
        self.errors = '%s-%s' % (errors, instance)

    def put(self, value):
        self.rediss.rpush(self.queue, value)

    def getError(self):
        item = self.rediss.lpop(self.errors)
        return item

    def getErrors(self):
        llen = self.rediss.llen(self.errors)
        count = 0
        ret = []
        if llen > 0:
            while count < llen:
                ret.append(self.getError())
                count += 1
        return ret