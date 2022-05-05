# import sqlite3 as sql
import pymssql as sql
import pandas as pd


class DataBaseReader(object):
    db = "DataElementsOfGameCompany"

    tables = dict()

    def __init__(self, host="(local)"):
        self.host = host
        self.conn = sql.connect(host=self.host, database=self.db)
        pass

    def GetCursor(self, msg: str):
        cur = self.conn.cursor()
        cur.excutive(msg)
        return cur

    def GetCompanyURLs(self):
        self.tables['company'] = pd.DataFrame(pd.read_sql("select * from company", self.conn))


tar = DataBaseReader()



