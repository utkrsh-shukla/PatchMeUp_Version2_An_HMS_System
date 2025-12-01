from celery import Celery
from celery.schedules import crontab
import os

def make_celery(app_name=__name__):
    broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    celery = Celery(app_name, broker=broker_url, backend=result_backend)
    celery.conf.update(
        task_serializer='json', accept_content=['json'], result_serializer='json',
        timezone='Asia/Kolkata', enable_utc=True,
        beat_schedule={
            'send-daily-reminders': {
                'task': 'app.tasks.reminders.send_daily_reminders',
                'schedule': crontab(hour=8, minute=0),
            },
            'generate-monthly-reports': {
                'task': 'app.tasks.reports.generate_monthly_reports',
                'schedule': crontab(day_of_month=1, hour=9, minute=0),
            },
        }
    )
    return celery

celery_app = make_celery()
