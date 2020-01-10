from celery import shared_task
from time import sleep
from random import randint
from .models import MessagesTable


@shared_task(bind=True)
def send_message(self, messenger, user_id, user_id_2, message):
    try:
        sleep(randint(1, 3))  # Имитация задержки отправки сообщения от 1 до 3 секунд.
        if randint(1, 10) == 10:  # 10% вероятность неудачной отправки.
            raise Exception
    except Exception as exc:
        raise self.retry(exc=exc, countdown=1, max_retries=5)  # В случае неудачи будет произведено еще 4 попытки отправки.
    MessagesTable.objects.create(messenger=messenger,
                                 sender_id=user_id,
                                 recipient_id=user_id_2,
                                 message=message)
    return "added message'" + message + "' from " + str(user_id) + " to " + str(user_id_2)
