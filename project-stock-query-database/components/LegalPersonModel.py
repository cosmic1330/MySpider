from middleware.orm.models import LegalPerson, DealDate, Stock
from middleware.orm.database import session
from datetime import datetime
from utils.delay import delay
import loguru
import requests
import json
from sqlalchemy import func
from decimal import Decimal
from bs4 import BeautifulSoup
import concurrent.futures





class LegalPersonModel:
    def __init__(self):
        pass

    def fetch(self, stock_id, stock_name):
        result = []
        try:
            # 取得最新資料
            r = requests.get(
                f'https://tw.stock.yahoo.com/quote/{stock_id}.TW/institutional-trading')
            # 將網頁資料以html.parser
            soup = BeautifulSoup(r.text, "html.parser")
            ul = soup.find_all('ul', class_="List(n)")
            lis = ul[1].find_all('li', class_="List(n)")
            for _, li in enumerate(lis):
                divs = li.find_all('div')
                if (len(divs) == 0):
                    break
                new_data = LegalPerson(
                    transaction_date=divs[1].text,
                    stock_id=stock_id,
                    stock_name=stock_name,
                    foreign_investors=int(divs[3].text.replace(',', ''))*1000,
                    investment_trust=int(divs[4].text.replace(',', ''))*1000,
                    dealer=int(divs[5].text.replace(',', ''))*1000,
                )
                result.append(new_data)
        except Exception as e:
            loguru.logger.error(
                f'[Fail] fetch {stock_id} legal person data, error:{e}')
        return result


    def query_lose_data_in_batchs(self):
        results = []
        batch_size=5
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        for i in range(0, len(stocks), batch_size):
            batch = stocks[i:i + batch_size]
            with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
       
                futures = [executor.submit(self.fetch, stock_id, stock_name) for (stock_id, stock_name) in batch]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
            
            # 在每个批次完成后打印结果
            print(f"Batch {i//batch_size + 1} results:")
            for result in results:
                print(result)
            results = []

    def query_lose_data(self):
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        for (stock_id, stock_name) in stocks:
            print(f"取得{stock_id} {stock_name}缺少的法人資料")
            try:
                # 取得最新資料
                r = requests.get(
                    f'https://tw.stock.yahoo.com/quote/{stock_id}.TW/institutional-trading')
                # 將網頁資料以html.parser
                soup = BeautifulSoup(r.text, "html.parser")
                ul = soup.find_all('ul', class_="List(n)")
                lis = ul[1].find_all('li', class_="List(n)")
                for _, li in enumerate(lis):
                    try:
                        divs = li.find_all('div')
                        if (len(divs) == 0):
                            break
                        new_data = LegalPerson(
                            transaction_date=divs[1].text,
                            stock_id=stock_id,
                            stock_name=stock_name,
                            foreign_investors=int(divs[3].text.replace(',', ''))*1000,
                            investment_trust=int(divs[4].text.replace(',', ''))*1000,
                            dealer=int(divs[5].text.replace(',', ''))*1000,
                        )
                        session.add(new_data)
                        session.commit()
                        print(f"[Success] create {stock_id} {stock_name} 『{divs[1].text}』 legal person data")
                    except Exception as e:
                        session.rollback()  # 回滾交易以清除未提交的更改
                        print(e)
                        loguru.logger.error(
                            f"[Skip] stockid:{stock_id} date:{divs[1].text} data:{new_data.__dict__}")
                        break
            except Exception as e:
                loguru.logger.error(
                    f'[Fail] create {stock_id} legal person data, error:{e}')

    def query_lose_data_twse(self):
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
                        foreign_investors=int(item[4].replace(',', '')) if item[4].replace(',', '').isdigit() else 0,
                        investment_trust=int(item[10].replace(',', '')) if item[10].replace(',', '').isdigit() else 0,
                        dealer=int(item[11].replace(',', '')) if item[11].replace(',', '').isdigit() else 0,
                    )
                    session.add(new_data)
                    session.commit()
                    print(f"[Success] create {item[0]} - {date[0]} data")
                except Exception as e:
                    session.rollback()
                    loguru.logger.error(f"無法添加對象「{item[0]}」，可能是因為重複鍵或其他完整性錯誤。, error:{e}')")
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
                    loguru.loggering(f"無法添加對象「{item[0]}」，可能是因為重複鍵或其他完整性錯誤。, error:{e}')")
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
            print(f'fail request {date} legal person data, error:{e}')