from middleware.orm.models import Taiex
from middleware.orm.database import session
from datetime import datetime
from utils.delay import delay
import loguru
import requests
from decimal import Decimal


class TaiexModel:
    def __init__(self):
        pass

    def query_lose_data(self):
        current_year = datetime.now().year
        current_month = datetime.now().month

        db_date = self.check_database_date()
        db_year = db_date[0].year
        db_month = db_date[0].month
        print("資料庫Taiex最大年月日:", db_date)

        # 刪除本月資料
        try:
            session.query(Taiex).filter(
                Taiex.year == current_year, Taiex.month == current_month).delete()

            # 寫入資料庫
            session.commit()
            loguru.logger.success('Success delete last month data')
        except Exception as e:
            # 發生例外錯誤，還原交易
            session.rollback()
            loguru.logger.error('Fail delete last month data')

        for year in range(db_year, current_year+1):
            for month in range(1, 13):

                if year == db_year and month < db_month:
                    continue
                if year == current_year and month > current_month:
                    break
                print(f"取得{year}年{month}月大盤交易資料")
                new_data = self.queryData(year, f"{month:02d}")
                for i in range(len(new_data)):
                    saving_date = datetime.strptime(
                        new_data[i].transaction_date, '%Y-%m-%d').date()
                    if (saving_date > db_date[0]):
                        try:
                            session.add(new_data[i])
                            session.commit()
                        except Exception as e:
                            session.rollback()
                            loguru.logger.error(
                                f'Fail create {new_data[i]} data')
                            print(e)
                            raise
                delay()
        loguru.logger.info(f"Create Taiex is done.")

    def check_database_date(self):
        return session.query(Taiex.transaction_date).order_by(Taiex.transaction_date.desc()).first()

    def check_taiex_count(self):
        return session.query(Taiex).count()

    def initial_taiex(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        year = 2010
        month = 1

        print(f"取得2010年1月-{current_year}年{current_month}月大盤交易資料")

        while year < current_year or month < current_month:
            print(f"取得{year}年{month}月大盤交易資料")
            new_data = self.queryData(year, f"{month:02d}")

            try:
                session.add_all(new_data)
                session.commit()
            except Exception as e:
                session.rollback()
                loguru.logger.error(f'Fail create {year}/{month} data')
                print(e)
                raise

            month += 1
            if month > 12:
                year += 1
                month = 1
            delay()
        loguru.logger.info(f"Initial Taiex is done.")

    @classmethod
    def queryData(self, year, month):
        try:
            # 連線
            headers = {
                'Content-Type': 'text/html; charset=utf-8'
            }
            r = requests.get(
                f"https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?date={year}{month}01&response=json", headers=headers)

            json_data = r.json()
            if 'data' in json_data:
                data = json_data['data']
                result = []
                for i in range(len(data)):
                    parts = data[i][0].strip().split("/")
                    year = int(parts[0]) + 1911  # 將民國年轉換為西元年
                    month = int(parts[1])
                    day = int(parts[2])
                    formatted_date = f"{year}-{month:02d}-{day:02d}"
                    result.append(Taiex(
                        transaction_date=formatted_date,
                        open_price=Decimal(data[i][1].replace(',', '')),
                        high_price=Decimal(data[i][2].replace(',', '')),
                        low_price=Decimal(data[i][3].replace(',', '')),
                        close_price=Decimal(data[i][4].replace(',', '')),
                    ))
                return result
            else:
                return []

        except Exception as e:
            loguru.logger.error(f'Fail query {year}/{month} data')
            raise
            print(e)
