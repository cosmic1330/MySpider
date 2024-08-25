from middleware.orm.models import LegalPerson, DealDate
from middleware.orm.database import session
from datetime import datetime
from utils.delay import delay
import loguru
import requests
import json
from sqlalchemy import func
from decimal import Decimal


class LegalPersonModel:
    def __init__(self):
        pass

    def query_lose_data(self):
        dealdate_last_date = session.query(DealDate.transaction_date).order_by(
            DealDate.transaction_date.desc()).first()
        legalperson_date = session.query(LegalPerson.transaction_date).order_by(
            LegalPerson.transaction_date.desc()).group_by(LegalPerson.transaction_date).first()
        print(f"取得『{legalperson_date}』-『{dealdate_last_date}』交易日期的法人資料")
        dates = session.query(DealDate.transaction_date).filter(
            DealDate.transaction_date > legalperson_date[0]).filter(
            DealDate.transaction_date <= dealdate_last_date[0]).all()
        for date in dates:
            data = self.queryData(date[0].strftime("%Y%m%d"))
            for item in data:
                try:
                    new_data = LegalPerson(
                        transaction_date=date[0],
                        stock_id=item[0],
                        stock_name=item[1].strip(),
                        foreign_investors=int(item[7].replace(',', '')) if item[7].replace(',', '').isdigit() else 0,
                        investment_trust=int(item[10].replace(',', '')) if item[10].replace(',', '').isdigit() else 0,
                        dealer=int(item[11].replace(',', '')) if item[11].replace(',', '').isdigit() else 0,
                    )
                    session.add(new_data)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    loguru.logger.warning(f"無法添加對象「{item[0]}」，可能是因為重複鍵或其他完整性錯誤。")
                    print(e)
            loguru.logger.success(f"{date[0]} legal person data create success")
            delay()
        loguru.logger.success("query legal person data success")

    def check_legal_person_count(self):
        return session.query(LegalPerson).count()

    def initial_legal_person(self):
        dealdate = session.query(DealDate.transaction_date).order_by(
            DealDate.transaction_date.asc()).all()
        for date in dealdate:
            data = self.queryData(date[0].strftime("%Y%m%d"))
            for item in data:
                try:
                    new_data = LegalPerson(
                        transaction_date=date[0],
                        stock_id=item[0],
                        stock_name=item[1].strip(),
                        foreign_investors=int(item[4].replace(',', '')) if item[4].replace(',', '').isdigit() else 0,
                        investment_trust=int(item[10].replace(',', '')) if item[10].replace(',', '').isdigit() else 0,
                        dealer=int(item[11].replace(',', '')) if item[11].replace(',', '').isdigit() else 0,
                        
                    )
                    session.add(new_data)
                    session.commit()
                except Exception as e:
                    session.rollback()  # 回滾事務
                    loguru.logger.warning(f"無法添加對象「{item[0]}」，可能是因為重複鍵或其他完整性錯誤。")
                    print(e)
            loguru.logger.success(f"{date[0]} legal person data create success")
            delay()
        loguru.logger.success("initial legal person data success")

    @staticmethod
    def queryData(date):
        url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={date}&selectType=ALLBUT0999&response=json&_=1689082835565"
        try:
            response = requests.get(url)
            if (response.json()['total'] == 0):
                return []
            else:
                return response.json()['data']
        except Exception as e:
            print(f'fail request {date} legal person data')
            print(e)
