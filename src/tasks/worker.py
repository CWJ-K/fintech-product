from celery import Celery

app = Celery(
    'task',
    include=['tasks'],
    # rabbitmq server: ip
    broker='pyamqp://worker:worker@localhost:5672/'
)