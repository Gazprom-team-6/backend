import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "backend.settings")

app = Celery("gazprom-id-6")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    """Функция для тестирования работы celery"""
    time.sleep(10)
    print("Hello task")
