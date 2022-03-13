"""
"""
import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re

passwd = input()

class Marketdata:
    def __init__(self):
        """DB연결 및 종목코드 Dictionary 생성"""
        print("Please identify to user")
        id = input()
        print("Please enter your password")
        passwrd = input()
        self.conn = pymysql.connect(host='localhost', user=id, passwd=passwrd, db='invest', charset='utf8')
        self.codes = {}
        self.get_comp_info()

    def __del__(self):
        """"소멸자: 연결 해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블 -> codes에 저장"""
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]

    def get_daily_price(self, code, start_date = None, end_date = None):
        """
        종목 별 시세를 Dataframe에 맞게 변환
        - code : KRX 종목코드 또는 상장기업명
        - start_date : 조회 시작일('2022-01-01') 미입력 시 1년 전 오늘
        - end_date : 조회 종료일('2022-02-02') 미입력 시 오늘
        """
    if (start_date is None):
        year_ago = datetime.today() - timedelta(days = 365)
        start_date = year_ago.strftime('%Y-%m-%d')
        print("start_date is initialized to = {}'".format(start_date))
    else:
        start_lst = re.split('\D+', start_date)
        if (start_lst[0] == ''):
            start_lst = start_lst[1:]
        start_year = int(start_lst[0])
        start_month = int(start_lst[1])
        start_day = int(start_lst[2])

        if sta
