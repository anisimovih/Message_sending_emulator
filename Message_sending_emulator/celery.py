import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Message_sending_emulator.settings')
celery_app = Celery('Message_sending_emulator')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
