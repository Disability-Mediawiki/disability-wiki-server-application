
# from celery import Celery
from time import sleep
from flask import current_app
import os
# from celery.utils.log import get_task_logger
# celery = Celery('task', backend="redis://localhost:6379",
#                 broker='redis://localhost:6379')
# logger = get_task_logger(__name__)

# celery.autodiscover_tasks()
from .CeleryService import celery
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@celery.task(bind=True)
# @celery.task
def task(self):
    file1 = open(os.path.join(
        current_app.config['ERROR_LOG_FILE']), 'a')
    file1.writelines("working from celelry")
    file1.close()
    logger.info('test logger working')
    sleep(5)
    print('LKASJDLKASJD')
    return "test reulsflkdsjafsklaflkjasdljsdlkafjlk;sjfdlkjsdflkj"
