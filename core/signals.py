from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_notifications_on_signup(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = 'user-notifications'
        event = {
            'type': 'user_joined',
            'text': instance.username
        }

        async_to_sync(channel_layer.group_send)(group_name, event)