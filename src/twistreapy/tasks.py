# Create your tasks here
from __future__ import absolute_import
from .models import Status, User, UserMention, Hashtag, URL
from dateutil.parser import parse
from celery.task import Task
from django.core.cache import cache
import sys

LOCK_EXPIRE = 60 * 5  # Lock expire 5 minutes


class PushService(Task):
    name = 'push.service'

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)

        lock_id = "%s-lock" % self.name

        acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)

        release_lock = lambda: cache.delete(lock_id)

        logger.debug("Starting Push Service")

        if acquire_lock():
            try:
                push_service()
            finally:
                release_lock()
            return

        logger.debug(
            "Push Service is Already Running"
        )
        return


class ImportService(Task):
    name = 'import.service'

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)

        lock_id = "%s-lock" % self.name

        acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)

        release_lock = lambda: cache.delete(lock_id)

        logger.debug("Starting Push Service")

        if acquire_lock():
            try:
                import_service(**kwargs)
            except:
                logger.exception(*sys.exc_info())
            finally:
                release_lock()
            return

        logger.debug(
            "Import Service is Already Running"
        )
        return


def push_service():
    import redis
    from django.conf import settings
    import json

    queue = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    for x in range(0, queue.llen(settings.REDIS_PUSH)):
        insert_status(json.loads(queue.blpop(settings.REDIS_PUSH)[1]))


def import_service(query, limit, offset=0, params=None):
    from .models import ImportHistory

    h = ImportHistory.objects.filter(sql=query)

    if h.count() == 0:
        if (limit - offset) > 100:
            limit = 100

    else:
        last = h.order_by('-created_at')[0]
        if offset > last.offset + 100:
            limit = 100
        elif (limit - (last.offset + 100)) < limit:
            limit = 100
            offset = last.offset + 100
        else:
            return False

    o = ImportHistory(sql=query, limit=limit, offset=offset)
    o.save()

    from django.db import connections
    from .cursor import to_dict

    args = {
        'limit': limit,
        'offset': offset
    }

    if type(params) is dict:
        args.update(**params)

    with connections['rest'].cursor() as cursor:
        cursor.execute(query, args)
        rows = to_dict(cursor)

    inserts = []
    errors = []

    for row in rows:
        row.pop('id')
        try:
            if import_tweet(row):
                inserts.append(row.get('id_tweet'))
        except:
            errors.append(row.get('id_tweet'))

    o.inserts_ids = inserts
    o.errors_ids = errors
    o.save()


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
    if Status.objects.filter(id=obj['id_tweet']).count():
        return False

    tweet = Status().import_dict(obj)

    from django.db import connections
    from .cursor import to_dict

    # Importar User Mentions
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM user_mentions
            WHERE id_tweet = %s
            """,
            [tweet.id]
        )
        user_mentions = to_dict(cursor)

    for um in user_mentions:
        UserMention().import_dict(um, tweet)

    # Importar Hashtags
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM hashtags
            WHERE id_tweet = %s
            """,
            [tweet.id]
        )
        hashtags = to_dict(cursor)

    for ht in hashtags:
        Hashtag().import_dict(ht, tweet)

    # Importar URLS
    with connections['rest'].cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM urls
            WHERE id_tweet = %s
            """,
            [tweet.id]
        )
        urls = to_dict(cursor)

    for ur in urls:
        URL().import_dict(ht, tweet)

    return True

    # instance, created = Status.objects.get_or_create(id=obj['id_tweet'])
    #
    # if not created:
    #     return False
    #
    # for k, v in list(obj.items()):
    #
    #     if k == 'id':
    #         pass
    #
    #     elif k == 'id_tweet':
    #         instance.id = v
    #
    #     elif k == 'id_user':
    #         user = User.objects.get_or_retrieve(uid=v)
    #
    #         instance.user = user
    #
    #     elif k == 'created_at':
    #         instance.created_at = parse(v)
    #
    #     elif hasattr(instance, k):
    #         instance.k = v.strip() if type(v) is unicode else v
    # instance.save(    #
    # import_entities(instance)


def import_entities(status):
    from django.db import connections
    from .cursor import to_dict
    from .models import Hashtag, UserMention, URL

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


