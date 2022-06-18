import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

begoacademy_app = Celery('config')
begoacademy_app.config_from_object('django.conf:settings', namespace='CELERY')
begoacademy_app.autodiscover_tasks()
