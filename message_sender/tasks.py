from celery import shared_task
from time import sleep
from random import randint
from .models import MessagesTable
import hashlib


@shared_task
def send_message(messenger, user_id, user_id_2, message):
    sleep(randint(1, 3))  # Имитация задержки отправки сообщения.
    MessagesTable.objects.create(messenger=messenger,
                                 sender_id=user_id,
                                 recipient_id=user_id_2,
                                 message=message)
    return str(user_id) + message
