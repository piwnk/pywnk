import pandas as pd
import pyodbc
import numpy as np

from .envs import SQL_SERVER_CONNECTION_STRING


class SqlConnector:
    def __init__(self, connection_string=SQL_SERVER_CONNECTION_STRING):
        self.connection_string = connection_string
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def __enter__(self, *args, **kwargs):
        # self.__init__(*args, **kwargs)
        return self

    def __exit__(self, *args):
        self.connection.close()
        print('Connection closed')

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


class SdeConnector(SqlConnector):
    def get_new_object_id(self, table):
        sql = """
            DECLARE @out int;
            EXEC sde.next_rowid ?, ?, @rowid = @out OUTPUT;
            SELECT @out AS objectid;
        """

        *_, user, table_name = table.split('.')
        result = self.exec(sql, user, table_name)
        return result.fetchone()[0]
