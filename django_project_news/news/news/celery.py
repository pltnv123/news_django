import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'print_every_7_days': {
        'task': 'appnews.tasks.email_every_monday',
        'schedule': crontab(day_of_week="monday", hour=0, minute=0),

    },
}

