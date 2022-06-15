import pandas as pd

from src.crawler.twse_crawler import (
    Period,
    TWSEWeb,
)


def test_generate_dates_in_a_period():

    result = (
        Period(
        start_date='2021-01-01',
        end_date='2021-01-05')
        .generate_dates_in_a_period()
    )
    expected = [
        '2021-01-01', '2021-01-02', '2021-01-03',
        '2021-01-04', '2021-01-05'
    ]

    assert (
        result == expected
    ) 


def test_twse_header():
    result = TWSEWeb('2022-01-01').request_header
    expected = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    assert result == expected