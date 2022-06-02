from celery import Celery

app = Celery(
    'task',
    include=['tasks'],
    broker='pyamqp://worker:worker@rabbitmq:5672/'
)