from celery import Celery
from config import Config


def make_celery(app_name):
    client = Celery(
        app_name,
        backend=Config.RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL,
    )
    client.autodiscover_tasks()
    return client
