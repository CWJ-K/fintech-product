from celery import Celery
from src.config import WORKER_ACCOUNT, WORKER_PASSWORD, MESSAGE_QUEUE_PORT, MESSAGE_QUEUE_PORT
# TODO into a list

app = Celery(
    'task',
    include=['src.tasks.task'],
    broker='pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@{MESSAGE_QUEUE_PORT}:{MESSAGE_QUEUE_PORT}/'
)
