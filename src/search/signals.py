from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import tweet_search
from .models import Tweet


@receiver(post_save, sender=Tweet)
def update_trigger(instance, created, **kwargs):
    if created:
        tweet_search(instance)
