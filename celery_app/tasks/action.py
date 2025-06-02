from celery_app.app import celery_app


@celery_app.task(queue='default')
def default_action():
    return 1
