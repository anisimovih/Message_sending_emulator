from celery import shared_task
from time import sleep
from random import randint


@shared_task
def send_message(user_id, message):
    sleep(randint(1, 3))  # Имитация задержки отправки сообщения.
    return str(user_id + message)
