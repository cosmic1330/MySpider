from middleware.orm.models import DailyDeal, Stock, DealDate
from middleware.orm.database import session
from datetime import datetime
from utils.delay import delay
import loguru
import requests
import json
from sqlalchemy import func
from decimal import Decimal


class DailyDealModel:
    def __init__(self):
        pass

    def query_lose_data(self):
        dealdate_last_date = session.query(DealDate.transaction_date).order_by(
            DealDate.transaction_date.desc()).first()
        dealdate_last_date=int(dealdate_last_date[0].strftime("%Y%m%d"))
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        for (stock_id, stock_name) in stocks:
            # check length of daily deal and last date
            last_date = session.query(
                DailyDeal.transaction_date,
            ).filter(
                DailyDeal.stock_id == stock_id
            ).order_by(
                DailyDeal.transaction_date.desc()
            ).first()

            transaction_count = session.query(DailyDeal).filter(
                DailyDeal.stock_id == stock_id).count()
            if(last_date is not None):
                last_date = int(last_date[0].strftime("%Y%m%d"))
                if(last_date != dealdate_last_date):
                    new_data = self.queryYahooData(
                        stock_id, stock_name, last_date, dealdate_last_date)
                    try:
                        session.add_all(new_data)
                        session.commit()
                        loguru.logger.info(
                            f"daily_deal stock {stock_id} {stock_name} 『{last_date}』－『{dealdate_last_date}』query success")
                    except Exception as e:
                        session.rollback()
                        loguru.logger.error(
                            f"daily_deal stock {stock_id} {stock_name} query fail")
                        loguru.logger.error(e)
                    
            elif last_date is None:
                new_data = self.queryYahooData(stock_id, stock_name)
                try:
                    session.add_all(new_data)
                    session.commit()
                    loguru.logger.info(
                        f"daily_deal stock {stock_id} {stock_name} initial success")
                except Exception as e:
                    session.rollback()
                    loguru.logger.error(
                        f"daily_deal stock {stock_id} {stock_name} initial fail")
                    loguru.logger.error(e)
        loguru.logger.info("get loss daily deal data done.")

    # query loss date from twse

    def check_daily_deal_count(self):
        return session.query(DailyDeal).count()

    def initial_daily_deal(self):
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        for (stock_id, stock_name) in stocks:
            new_data = self.queryYahooData(stock_id, stock_name)
            try:
                session.add_all(new_data)
                session.commit()
                loguru.logger.info(
                    f"stock {stock_id} {stock_name} initial success")
            except Exception as e:
                session.rollback()
                loguru.logger.error(
                    f"stock {stock_id} {stock_name} initial fail")
                loguru.logger.error(e)
        loguru.logger.info("initial daily deal data success")

    @classmethod
    def queryYahooData(self, stock_id, stock_name, start_date=None, end_date=None):
        url = f"https://tw.quote.finance.yahoo.net/quote/q?type=ta&perd=d&mkt=10&sym={stock_id}&v=1&callback="
        try:
            response = requests.get(url)
            json_string = response.text.replace("(", "").replace(");", "")
            data = json.loads(json_string)['ta']
            if (start_date is None and end_date is None):
                result = [
                    DailyDeal(transaction_date=f"{str(item['t'])[:4]}-{str(item['t'])[4:6]}-{str(item['t'])[6:]}",
                              stock_id=stock_id,
                              stock_name=stock_name,
                              volume=int(item['v']),
                              open_price=Decimal(item['o']),
                              close_price=Decimal(item['c']),
                              high_price=Decimal(item['h']),
                              low_price=Decimal(item['l']),)
                    for item in data]
            else:
                result = [
                    DailyDeal(transaction_date=f"{str(item['t'])[:4]}-{str(item['t'])[4:6]}-{str(item['t'])[6:]}",
                              stock_id=stock_id,
                              stock_name=stock_name,
                              volume=int(item['v']),
                              open_price=Decimal(item['o']),
                              close_price=Decimal(item['c']),
                              high_price=Decimal(item['h']),
                              low_price=Decimal(item['l']),)
                    for item in data if start_date < item['t'] <= end_date]
            return result
        except Exception as e:
            print(f'fail request {stock_id} yahoo data')
            print(e)

    def queryTwseData(self, date, stock_id):
        url=f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_id}"
        pass
