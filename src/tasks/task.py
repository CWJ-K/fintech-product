import importlib
from typing import  Dict

from src.backend import db
from src.tasks.worker import app

@app.task()
def crawler(dataset: str, parameter: Dict[str, str]):
    data = getattr(
        importlib.import_module(f'src.crawler.{dataset}'),
        'crawler',
    )(parameter=parameter)
    db.upload_data(data, dataset, db.router.mysql_financialdata_conn)
