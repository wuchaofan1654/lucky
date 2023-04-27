import datetime
import os
import time

from django.conf import settings
from celery import platforms
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery(f"application", broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2')

app.conf.timezone = "Asia/Shanghai"
app.conf.beat_schedule = {
    'send_message_period': {
        'task': 'system.tasks.websocket_push',
        'schedule': 3600,
        'args': (1, "content sent by beat_schedule ~")
    },
}


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


