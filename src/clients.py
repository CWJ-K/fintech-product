from sqlalchemy import create_engine, engine
from sqlalchemy.engine.base import Connection


def get_mysql_financialdata_conn() -> Connection:
    address = 'mysql+pymysql://root:root@139.162.60.41:3306/financialdata'
    enginer = create_engine(address)
    connect = engine.connect()
    return connect