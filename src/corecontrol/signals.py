from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Configuration, ConfigurationSync


@receiver(post_save, sender=Configuration)
def update_trigger(instance, **kwargs):
    sync, created = ConfigurationSync.objects.get_or_create(configuration=instance)
    try:
        r = requests.get(
            "http://%s:5000/update" % instance.server.ip,
            auth=('admin', 'secret'),
            timeout=30
        )
    except requests.ConnectionError, requests.ConnectTimeout:
        sync.status = 'ER'
        sync.save()
        return None
    if r.status_code != 200:
        sync.status = 'UK'
        sync.save()
        return None
    sync.status = 'OK'
    sync.save()
