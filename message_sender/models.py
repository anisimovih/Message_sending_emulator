from django.db import models
from .managers import MessageManager


class MessagesTable(models.Model):

    messenger = models.CharField(max_length=50)
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField()
    message = models.CharField(max_length=400)
    objects = MessageManager()

    class Meta:
        indexes = [models.Index(fields=['sender_id', 'recipient_id', 'messenger'])]
