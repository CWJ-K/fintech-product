import importlib
from typing import  Dict

from src.backend import db
from src.tasks.worker import app

@app.task()
def crawler(crawler_name: str, date: str):
    data = getattr(
        importlib.import_module(f'src.crawler.{crawler_name}'),
        'produce_daily_report',
    )(date=date)
    db.upload_data(data, crawler_name, db.router.mysql_financialdata_conn)
