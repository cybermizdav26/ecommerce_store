from __future__ import absolute_import, unicode_literals
import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_store.settings')

app = Celery('ecommerce_store')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request}")


@app.task(bind=True)
def add(self, x, y):
    time.sleep(5)
    print(f"Adding {x} and {y}")
    return x + y


@app.task(bind=True)
def multiply(self, x, y):
    print(f"Multiply {x} and {y}")
    return x * y
