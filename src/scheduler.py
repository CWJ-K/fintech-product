import time
import datetime

from apscheduler.schedulers.background import (
    BackgroundScheduler,
)
from src.producer import (
    Update,
)
from loguru import logger


def send_crawler_task():
    today = (
        datetime.datetime.today()
        .date()
        .strftime("%Y-%m-%d")
    )
    Update(
        dataset="twse_crawler",
        start_date=today,
        end_date=today,
    )


def main():
    scheduler = BackgroundScheduler(
        timezone="Asia/Taipei"
    )
    scheduler.add_job(
        id="send_crawler_task",
        func=send_crawler_task,
        trigger="cron",
        hour="15",
        minute="0",
        day_of_week="mon-fri",
    )
    logger.info("send_crawler_task")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)