from celery import Celery
from flask import current_app


def make_celery():
    celery = Celery(
        "celery_test",
        backend='redis://localhost:6379',
        broker='redis://localhost:6379'
    )
    # celery.conf.update(current_app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with current_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task()
def add_together(a, b):
    f = open("myfile.txt", "w")
    f.writelines("asd")
    f.close()
    return a + b


argv = [
    'worker'
]
celery.worker_main(argv)
