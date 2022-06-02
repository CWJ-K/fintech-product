import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine
from api import config


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f'mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}'
        f'@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}'
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect

app = FastAPI()


@app.get("/")
def read_root():
    return {'Hello': 'World'}


@app.get('/taiwan_stock_price')
def taiwan_stock_price(
    stock_id: str = "",
    start_date: str = "",
    end_date: str = "",
):
    sql = f"""
    SELECT * FROM taiwan_stock_price
    WHERE StockID = '{stock_id}'
    and Date >= '{start_date}'
    and Data <= '{end_date}'
    """
    mysql_conn = get_mysql_financialdata_conn()
    raw_data = pd.read_sql(sql, con=mysql_conn)
    data = raw_data.to_dict('records')
    return {'data': data}

