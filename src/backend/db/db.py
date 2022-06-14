import typing

import pandas as pd
import pymysql
from loguru import logger
from sqlalchemy import engine


def update_data_to_mysql_by_pandas(
    df: pd.DataFrame,
    table: str,
    mysql_connection: engine.base.Connection,
):
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_connection,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
        except Exception as e:
            logger.info(e)
            return False
    return True


def build_update_sql(
    colname: typing.List[str],
    value: typing.List[str],
):
    update_sql = ",".join(
        [
            ' `{}` = "{}" '.format(
                colname[i],
                str(value[i]),
            )
            for i in range(len(colname))
            if str(value[i])
        ]
    )
    return update_sql


def build_df_update_sql(
    table: str, df: pd.DataFrame
) -> typing.List[str]:
    logger.info("build_df_update_sql")
    df_columns = list(df.columns)
    sql_list = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        value = [
            pymysql.converters.escape_string(
                str(v)
            )
            for v in temp
        ]
        sub_df_columns = [
            df_columns[j]
            for j in range(len(temp))
        ]
        update_sql = build_update_sql(
            sub_df_columns, value
        )

        sql = """INSERT INTO `{}`({})VALUES ({}) ON DUPLICATE KEY UPDATE {}
            """.format(
            table,
            "`{}`".format(
                "`,`".join(
                    sub_df_columns
                )
            ),
            '"{}"'.format(
                '","'.join(value)
            ),
            update_sql,
        )
        sql_list.append(sql)
    return sql_list


def update_data_to_mysql_by_sql(
    df: pd.DataFrame,
    table: str,
    mysql_connection: engine.base.Connection,
):
    sql = build_df_update_sql(table, df)
    commit(
        sql=sql, mysql_connection=mysql_connection
    )


def commit(
    sql: typing.Union[
        str, typing.List[str]
    ],
    mysql_connection: engine.base.Connection = None,
):
    logger.info("commit")
    try:
        trans = mysql_connection.begin()
        if isinstance(sql, list):
            for s in sql:
                try:
                    mysql_connection.execution_options(
                        autocommit=False
                    ).execute(
                        s
                    )
                except Exception as e:
                    logger.info(e)
                    logger.info(s)
                    break

        elif isinstance(sql, str):
            mysql_connection.execution_options(
                autocommit=False
            ).execute(
                sql
            )
        trans.commit()
    except Exception as e:
        trans.rollback()
        logger.info(e)


def upload_data(data: pd.DataFrame, table: str, my_sql_connection: engine.base.Connection) -> None:
    if len(data) > 0:
        if update_data_to_mysql_by_pandas(
            data=data, table=table, mysql_connection=my_sql_connection
        ):
            pass
        else:
            update_data_to_mysql_by_sql(
                data= data, table=table, mysql_connection=my_sql_connection
            )
        
