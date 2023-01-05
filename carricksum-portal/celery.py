# yourvenv/cfehome/celery.py
from __future__ import absolute_import, unicode_literals # for python2

import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carricksum-portal.settings')

import os
from celery import Celery

BASE_SQS_URL = os.getenv('SQS_URL')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery('carricksum-portal')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_SQS_URL

app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_CONFIG = {
    "CELERY_TASK_SERIALIZER": "json",
    "CELERY_ACCEPT_CONTENT": ["json"],
    "CELERY_RESULT_SERIALIZER": "json",
    "CELERY_RESULT_BACKEND": None,
    "CELERY_TIMEZONE": "America/Sao_Paulo",
    "CELERY_ENABLE_UTC": True,
    "CELERY_ENABLE_REMOTE_CONTROL": False,
}
BROKER_URL = BASE_SQS_URL,
CELERY_CONFIG.update(
    **{
        "BROKER_URL": BROKER_URL,
        "BROKER_TRANSPORT": "sqs",
        "BROKER_TRANSPORT_OPTIONS": {
            "region": "us-west-2",
            "visibility_timeout": 3600,
            "polling_interval": 60,
        },
    }
)
app.conf.update(**CELERY_CONFIG)

