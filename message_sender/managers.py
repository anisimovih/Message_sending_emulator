from django.db import models
from django.db import connection


class MessageManager(models.Manager):
    @staticmethod
    def check_existence_by_text(messenger, sender_id, recipient_id, message_text):
        with connection.cursor() as cursor:
            cursor.execute("""
                select exists 
                (
                    select message from message_sender_messagestable 
                    where messenger = %s and sender_id = %s and recipient_id = %s and message = %s
                )
                """, (messenger, sender_id, recipient_id, message_text))
            for row in cursor:
                return row[0]
