import pymysql
class DBUpdater:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='ghost@0@', db='Invest', charset='utf8')
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info(
	        code VARCHAR(20),
	        company VARCHAR(40),
	        last_update DATE,
	        PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily(
	        code VARCHAR(20),
	        date DATE,
	        open BIGINT(20),
	        high BIGINT(20),
	        low BIGINT(20),
	        close BIGINT(20),
	        diff BIGINT(20),
	        vol BIGINT(20),
	        PRIMARY KEY (code, date)
            """
            curs.execute(sql)
            self.conn.commit()
            self.codes = dict()
            self.update_comp_info()
        def __del__(self):
            self.conn.close()

import pandas as pd
from datetime import datetime

class DBUpdater:
    def update_comp_info(self):
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]]=df['company'].values[idx]
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last"\
                            "_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}) {idx:04d} REPLACE INTO company_info "\
                          "VALUES ({code}, {company}, {today})")
                    self.conn.commit()
                    print('')