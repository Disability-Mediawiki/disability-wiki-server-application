from celery import Celery
from time import sleep
from celery.utils.log import get_task_logger
celery = Celery('task', backend="redis://localhost:6379",
                broker='redis://localhost:6379')
logger = get_task_logger(__name__)
celery.autodiscover_tasks()
