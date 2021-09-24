class DBupdate;
    def __init__(self):
    def __del__(self):
    def read_krx_ticker(self):
    def update_comp_info(self):
    def read_naver(self, code, company, pages_to_fetch):
    def replace_into_db(self, df, num, code, company):
    def update_daily_price(self, pages_to_fetch):
    def excu_daily(self):

if __name__ == '__main__':
    dbu = DBupdate()
    dbu.excu_daily()