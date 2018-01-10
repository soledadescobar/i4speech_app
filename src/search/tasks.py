# Create your tasks here
from __future__ import absolute_import
# from celery import shared_task
from celery.decorators import task
import redis
import json
import time
from corecontrol.api import get_active_api as get_api
from .models import Tweet, TweetResult
from twistreapy.models import Status
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


@task(name="tweet_search")
def tweet_search(obj):
    connect_redis()
    api = get_api(endpoint='tweets')
    try:
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
    except:
        time.sleep(5)
        tweet_search(obj)
        return None
    if not len(search):
        return False
    ids = store_search(search, TweetResult, obj)
    if not obj.max_id or obj.max_id < ids[-1]:
        obj.max_id = ids[-1]
    if not obj.since_id or obj.since_id > ids[0]:
        obj.since_id = ids[0]
    obj.save()
    if obj.results_count() < obj.max_results:
        tweet_search.delay(obj)


def store_search(result, model, obj):
    ids = []
    for r in result:
        status = r.AsDict()
        queue.rpush('streamb', json.dumps(status))
        res = model(
            tweet=obj,
            screen_name=status.get('user')['screen_name'],
            result_id=status.get('id')
        )
        res.save()
        ids.append(status['id'])
    return sorted(ids, key=int)


@task(name="tweet_search_v2")
def tweet_search_v2(obj):
    connect_redis()
    api = get_api(endpoint='tweets')
    try:
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
    except:
        time.sleep(5)
        tweet_search(obj)
        return None
    if not len(search):
        return False
    ids = store_search_v2(search, TweetResult, obj)
    if not obj.max_id or obj.max_id < ids[-1].id:
        obj.max_id = ids[-1].id
    if not obj.since_id or obj.since_id > ids[0].id:
        obj.since_id = ids[0].id
    obj.save()
    if obj.results_count() < obj.max_results:
        tweet_search.delay(obj)


def store_search_v2(result, model, obj):
    created = []
    for r in result:
        created.append(
            Status().parse_dict(
                r.AsDict()
            )
        )

    return created

