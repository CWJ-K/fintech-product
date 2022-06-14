import time
from typing import Callable

from loguru import logger
from sqlalchemy import engine
from sqlalchemy.engine.base import Connection
from src.backend.db import clients


def check_alive(connect: Connection):
    connect.execute('SELECT 1 + 1')


def reconnect(connect_func: Callable) -> Connection:
    try:
        connect = connect_func()
    except Exception as e:
        logger.info(
            f'{connect_func.__name__} reconnect error {e}'
        )
    return connect


def check_connect_alive(connect: Connection, connect_func: Callable):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(
                f'{connect_func.__name__} connect, error: {e}'
            )
            time.sleep(1)
            connect = reconnect(connect_func)
            return check_connect_alive(
                connect, connect_func
            )
    else:
        connect = reconnect(connect_func)
        return check_connect_alive(connect, connect_func)


class Router:
    def __init__(self):
        self._mysql_invest_connection = clients.get_mysql_invest_connection()

    def check_mysql_invest_connection_alive(self):
        self._mysql_invest_connection = check_connect_alive(
            self._mysql_invest_connection,
            clients.get_mysql_invest_connection,
        )
        return self._mysql_invest_connection

    @property
    def mysql_invest_connection(self):
        self.check_mysql_invest_connection_alive()
        return self._mysql_invest_connection

    def close_connection(self):
        self._mysql_invest_connection.close()

