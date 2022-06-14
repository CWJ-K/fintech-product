from sqlalchemy import create_engine, engine
from sqlalchemy.engine.base import Connection


def get_mysql_invest_connection() -> Connection:
    address = 'mysql+pymysql://user:user@localhost:3306/invest'
    engineer = create_engine(address)
    connect = engineer.connect()
    return connect