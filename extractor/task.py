from celery import Celery
from time import sleep
app =Celery('task', broker="redis://localhost:6379")

@app.task
def test():
    sleep(5)
    print('hello')