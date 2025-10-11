from celery import Celery

from .config import settings


def create_celery():
    celery_app = Celery()
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app


celery_app = create_celery()
