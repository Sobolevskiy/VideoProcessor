from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Video(models.Model):
    file = models.FileField(upload_to='video/%Y/%m/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)


@receiver(pre_delete, sender=Video)
def video_delete(sender, instance, **kwargs):
    instance.file.delete(False)
