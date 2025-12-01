@echo off
echo ============================================================
echo Starting Celery Worker for Hospital Management System
echo ============================================================
echo.
echo Make sure Redis is running on localhost:6379
echo.
echo Starting Celery worker...
echo Press CTRL+C to stop the worker
echo ============================================================
echo.

celery -A celery_worker.celery_app worker --loglevel=info --pool=solo