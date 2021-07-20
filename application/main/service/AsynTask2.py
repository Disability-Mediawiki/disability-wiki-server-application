
from celery import Celery
from time import sleep
from celery.utils.log import get_task_logger
celery = Celery('task',  broker='redis://localhost:6379')
logger = get_task_logger(__name__)


# @celery.task(bind=True)
# @celery.task
# def task():
#     print('LKASJDLKAasdasdsadSJD')
#     logger.info('test logger working')
#     sleep(5)
#     print('LKASJDLKASJD')


def printtest(text):
    print('hello world')
    sleep(5)
    return 'LKASJDLKASJD'
