from celery import Celery

from core.config import config

celery_app = Celery(
    'celery_app.celery_app',
    broker=config.rabbit_mq.url,
    backend='rpc://',
    broker_connection_retry_on_startup=True,
    include=[
        'celery_app.tasks.action'
    ]
)
