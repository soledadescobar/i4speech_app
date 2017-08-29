from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Configuration
from .tasks import configuration_sync


@receiver(post_save, sender=Configuration)
def update_trigger(instance, **kwargs):
    configuration_sync.delay(instance)
