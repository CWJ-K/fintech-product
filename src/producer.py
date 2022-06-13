import importlib
import sys

from loguru import logger

from src.backend import db
from src.tasks.task import crawler


def Update(crawler_name: str, start_date: str, end_date: str):
    dates = getattr(
        importlib.import_module(f'src.crawler.{crawler_name}'),
        'Period',
    )(start_date=start_date, end_date=end_date).generate_dates_in_a_period()
    
    for date in dates:
        logger.info(f'{crawler_name}, {date}') 
        task = crawler.s(crawler_name, date)
        
        task.apply_async(queue=crawler_name)
    
    db.router.close_connection()

if __name__ == '__main__':
    crawler_name, start_date, end_date = sys.argv[1:]
    Update(crawler_name, start_date, end_date)
