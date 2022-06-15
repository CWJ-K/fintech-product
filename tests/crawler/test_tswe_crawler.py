import pandas as pd

from src.crawler.twse_crawler import (
    Period
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