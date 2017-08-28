# Create your tasks here
from __future__ import absolute_import
# from celery import shared_task
from celery.decorators import task
import redis
import json
from corecontrol.api import get_active_api as get_api
from .models import Tweet, TweetResult
from django.conf import settings


queue = None


def connect_redis():
    global queue
    if not queue:
        queue = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )


@task(name="Busqueda de Tweets")
def tweet_search(obj):
    connect_redis()
    api = get_api(endpoint='tweets')
    search = api.GetSearch(
        term=obj.term,
        raw_query=obj.raw_query,
        since=obj.since,
        until=obj.until,
        since_id=obj.since_id,
        max_id=obj.max_id,
        count=100,
        include_entities=True
    )
    if not len(search):
        return False
    ids = store_search(search, TweetResult, obj)
    if not obj.max_id or obj.max_id < ids[-1]:
        obj.max_id = ids[-1]
    if not obj.since_id or obj.since_id > ids[0]:
        obj.since_id = ids[0]
    obj.save()
    if obj.results_count() < obj.max_results:
        tweet_search(obj)


def store_search(result, model, obj):
    ids = []
    for r in result:
        status = r.AsDict()
        queue.rpush('stream-v2', json.dumps(status))
        res = model(
            tweet=obj,
            screen_name=status.get('user')['screen_name'],
            result_id=status.get('id')
        )
        res.save()
        ids.append(status['id'])
    return sorted(ids, key=int)
