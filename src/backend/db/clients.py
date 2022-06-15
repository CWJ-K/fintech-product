from sqlalchemy import create_engine, engine
from sqlalchemy.engine.base import Connection
from src import config


def get_mysql_invest_connection() -> Connection:
    address = (
        f'mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}'
        f'@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}'
    )
    engineer = create_engine(address)
    connect = engineer.connect()
    return connect