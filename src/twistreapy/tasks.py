# Create your tasks here
from __future__ import absolute_import
from celery.decorators import task
from .models import Status, User
from dateutil.parser import parse


@task(name='push_service')
def push_service():
    import redis
    from django.conf import settings
    import json

    queue = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    while True:
        insert_status(json.loads(queue.blpop(settings.REDIS_PUSH)[1]))


def insert_status(obj):
    if obj.get('delete', False):
        # TODO Loguear un delete de tweet detectado por el stream
        return False
    else:
        Status().parse_dict(obj)


def insert_user(obj):
    values = {}
    instance = User()
    for k, v in list(obj.items()):
        if k == 'created_at':
            values['created_at'] = parse(v)
        elif hasattr(instance, k):
            values[k] = v
    instance, created = User.objects.get_or_create(defaults=values, id=obj['id'])
    if created:
        instance.save()
    return instance


# Metodo exclusivo para realizar importacion de tweets desde los modelos de base anteriores
def import_tweet(obj):
    instance, created = Status.objects.get_or_create(id=obj['id_tweet'])

    if not created:
        return False

    for k, v in list(obj.items()):

        if k == 'id':
            pass

        elif k == 'id_tweet':
            instance.id = v

        elif k == 'id_user':
            user = User.objects.get_or_retrieve(uid=v)

            instance.user = user

        elif k == 'created_at':
            instance.created_at = parse(v)

        elif hasattr(instance, k):
            instance.k = v.strip() if type(v) is unicode else v
    instance.save()

    import_entities(instance)

    return True


def import_entities(status):
    from django.db import connections
    from rest.cursor import to_dict
    from .models import Hashtag, UserMention, Media, URL

    # Buscar hashtags
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            'SELECT * FROM hashtags WHERE id_tweet = %s',
            [status.id]
        )
        hashtags = to_dict(cursor)

    # Buscar user_mentions
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            'SELECT * FROM user_mentions WHERE id_tweet = %s',
            [status.id]
        )
        user_mentions = to_dict(cursor)

    # Buscar media
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            'SELECT * FROM media WHERE id_tweet = %s',
            status.id
        )
        media = to_dict(cursor)

    # Buscar URLS
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            'SELECT * FROM urls WHERE id_tweet = %s',
            [status.id]
        )
        urls = to_dict(cursor)

    # Insertar Hashtags
    for h in hashtags:
        obj = Hashtag()
        obj.indices = h['indices'].strip()
        obj.text = h['text'].strip()
        obj.status = status
        obj.save()

    for u in user_mentions:
        obj = UserMention()
        obj.indices = u['indices'].strip()
        obj.name = u['name'].strip()
        obj.screen_name = u['screen_name'].strip()
        obj.user = User.objects.get_or_retrieve(uid=u['id_user_mentions'])
        obj.status = status
        obj.save()


