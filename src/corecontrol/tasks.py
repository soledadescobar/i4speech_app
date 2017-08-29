# Create your tasks here
from __future__ import absolute_import
# from celery import shared_task
import requests
from celery.decorators import task
from .models import ConfigurationSync


@task(name="configuration_sync")
def configuration_sync(obj):
    sync, created = ConfigurationSync.objects.get_or_create(configuration=obj)
    try:
        r = requests.get(
            "http://%s:5000/update" % obj.server.ip,
            auth=('admin', 'secret'),
            timeout=30
        )
    except (requests.ConnectionError, requests.ConnectTimeout):
        sync.status = 'ER'
        sync.save()
        return None
    if r.status_code != 200:
        sync.status = 'UK'
        sync.save()
        return None
    sync.status = 'OK'
    sync.save()

