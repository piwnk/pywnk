import pandas as pd
import pyodbc
import numpy as np

from .envs import SQL_SERVER_CONNECTION_STRING


def select(query, connection_string=SQL_SERVER_CONNECTION_STRING):
    # print(query)
    sql_conn = pyodbc.connect(connection_string)
    df = pd.read_sql(query, sql_conn)
    sql_conn.close()
    return df


def insert(table, fields, rows, connection_string=SQL_SERVER_CONNECTION_STRING):
    fields_len = len(fields)
    if not all(len(row) == fields_len for row in rows):
        raise Exception("row lengts different than fields count")

    sql_conn = pyodbc.connect(connection_string)
    cursor = sql_conn.cursor()

    rows_unnumpyed = [
        [int(v) if type(v) == np.int64 else v for v in row]
        for row in rows
    ]
    values_placeholder = ','.join(fields_len * "?")
    sql = f"insert into {table} ({','.join(fields)}) values ({values_placeholder})"
    print(sql)
    cursor.executemany(sql, rows_unnumpyed)
    cursor.commit()
    sql_conn.close()


class SQL_CONNECTOR:
    def __init__(self, connection_string=SQL_SERVER_CONNECTION_STRING):
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def select(self, table, fields="*", clauses=""):
        if isinstance(fields, list):
            fields = ','.join(fields)
        sql = f"select {fields} from {table} {clauses}"
        df = pd.read_sql(sql, self.connection)
        return df

    def exec(self, *args, **kwargs):
        result = self.cursor.execute(*args, **kwargs)
        self.cursor.commit()
        return result

    def insert(self, table, fields, rows):
        fields_len = len(fields)
        if not all(len(row) == fields_len for row in rows):
            raise Exception("row lengts different than fields count")

        values_placeholder = ','.join(fields_len * "?")
        rows_unnumpyed = [
            [int(v) if type(v) == np.int64 else v for v in row]
            for row in rows
        ]

        sql = f"insert into {table} ({','.join(fields)}) values ({values_placeholder})"
        self.cursor.executemany(sql, rows_unnumpyed)
        self.cursor.commit()

    def delete(self, table, where="1=1"):
        sql = f"delete from {table} where {where}"
        if where == "1=1":
            user_answer = input('All rows will be deleted. Are you sure?')
            if user_answer not in ['y', 'yes', 't', 'tak']:
                print('Interrupted')
                return

        self.exec(sql)


class SDE_CONNECTOR(SQL_CONNECTOR):
    def get_new_object_id(self, table):
        sql = """
            DECLARE @out int;
            EXEC sde.next_rowid ?, ?, @rowid = @out OUTPUT;
            SELECT @out AS objectid;
        """

        *_, user, table_name = table.split('.')
        result = self.exec(sql, user, table_name)
        return result.fetchone()[0]
