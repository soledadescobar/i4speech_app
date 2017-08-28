from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Candidato


@receiver(post_save, sender=Candidato)
def update_trigger(instance, created, **kwargs):
    if not created and instance.user_id:
        return False

    import corecontrol.api as api

    api.get_active_api(endpoint='user')

    user = api.api.GetUser(screen_name=instance.screen_name).AsDict()

    if user:
        instance.user_id = user['id']
        instance.save()
