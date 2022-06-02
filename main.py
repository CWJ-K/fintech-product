import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine

app = FastAPI()

@app.get("/")
def read_root():
    return {'Hello': 'World'}


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = 'mysql+pymysql://root:root@127.0.0.1:3306/financialdata'
    engine = create_engine(address)
    connect = engine.connect()
    return connect


@app.get('/taiwan_stock_price')
def taiwan_stock_price(
    stock_id: str = "",
    start_date: str = "",
    end_date: str = ""
):
    sql = f"""
        SELECT * FROM TaiwanStockPrice
        WHERE StockID = '{stock_id}'
        and Date >= '{start_date}'
        and Date <= '{end_date}'
    """
    mysql_conn = get_mysql_financialdata_conn()
    raw_data = pd.read_sql(sql, con=mysql_conn)
    data = raw_data.to_dict("records")
    return {'data': data}

