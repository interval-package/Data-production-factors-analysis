# import sqlite3 as sql
import pymssql as sql
import pandas as pd


class DataBaseReader(object):
    db = "data_factors"

    tables = dict()

    def __init__(self, host="(local)"):
        self.host = host
        self.conn = sql.connect(host=self.host, database=self.db)

        pass

    def GetCursor(self, msg: str):
        cur = self.conn.cursor()
        cur.excutive(msg)
        return cur

    def insert(self, tab: str, data: list):
        try:
            with self.conn.cursor() as cur:
                cur.excutive("""
                insert into {}
                values({},{})
                """.format(tab, data[0], data[1]))
        except Exception as e:
            print(repr(e))
        pass

    def GetCompanyURLs(self):
        self.tables['company'] = pd.DataFrame(pd.read_sql("select * from company", self.conn))


tar = DataBaseReader()
