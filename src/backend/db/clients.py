from sqlalchemy import create_engine, engine
from sqlalchemy.engine.base import Connection


def get_mysql_financialdata_conn() -> Connection:
    address = 'mysql+pymysql://user:user@localhost:3306/stock'
    enginer = create_engine(address)
    connect = enginer.connect()
    return connect