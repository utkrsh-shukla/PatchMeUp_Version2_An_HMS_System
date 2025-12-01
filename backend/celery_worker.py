"""Celery worker entry point"""
from app import create_app
from app.celery_config import celery_app
from app import db

# Create Flask app for context
flask_app = create_app()

# Configure Celery to use Flask app context
class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask

# Import tasks to register them
from app.tasks import send_daily_reminders, generate_monthly_reports, export_patient_treatments

if __name__ == '__main__':
    celery_app.start()
