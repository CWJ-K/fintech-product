from celery import Celery
from src.config import WORKER_ACCOUNT, WORKER_PASSWORD, MESSAGE_QUEUE_HOST, MESSAGE_QUEUE_PORT

app = Celery(
    'task',
    include=['src.tasks.task'],
    broker=f'pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/'
)
