import requests
from datetime import datetime, timedelta
from middleware.orm.models import Stock
from middleware.orm.database import session
import loguru
from bs4 import BeautifulSoup


class StocksModel:
    def __init__(self):
        pass

    def check_stockid_count(self):
        return session.query(Stock).count()

    def refresh_current_stockIds(self):
        # get database stock ids
        try:
            ids = session.query(Stock).all()
            session.query(Stock).update({Stock.enabled: False, Stock.listed: False})
            session.commit()
        except Exception as e:
            session.rollback()
            loguru.logger.error('Fail update stock disabled, error:{e}')

        # create new stock ids
        datas1 = self.getListedStockIds()
        datas2 = self.getOtcStockIds()
        datas = datas1 + datas2
        for data in datas:
            new_stock = Stock(
                stock_id=data['stock_id'],
                stock_name=data['stock_name'],
                enabled=data['enabled'],
                listed=data['listed'],
            )
            try:
                session.add(new_stock)
                session.commit()
            except Exception as e:
                session.rollback()
                try:
                    session.query(Stock).filter(
                        Stock.stock_id == data['stock_id']).update({Stock.enabled: True, Stock.listed: data['listed']})
                    session.commit()
                except Exception as e:
                    session.rollback()
                    loguru.logger.error(
                        f'Fail create stock id {data["stock_id"]} {data["stock_name"]}, error:{e}')

        loguru.logger.info(f"stocks id update is done.")

    @staticmethod
    def getListedStockIds():
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?response=json&_=1688900750130"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()['data']
            result = [{
                'stock_id': item[0],
                'stock_name': item[1],
                'enabled': True,
                'listed': True,
            } for item in data]

            return result
        except Exception as e:
            print('fail request stock ids')
            print(e)

    @staticmethod
    def getOtcStockIds():
        current_date = datetime.now()
        # 检查今天是否是假日（周六或周日）
        if current_date.weekday() == 5:  # 周六
            current_date -= timedelta(days=1)
        elif current_date.weekday() == 6:  # 周日
            current_date -= timedelta(days=2)
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        print(f"取得{current_year-1911}年{current_month}月{current_day}日上櫃股票代號")
        url = f"https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=htm&d={current_year-1911}/{current_month:02d}/{current_day:02d}&c=&s=0,asc"
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find('table')
            tbody = table.find('tbody')
            trs = tbody.find_all('tr')
            result = []
            for tr in trs:
                tds = tr.find_all('td')
                temp = {
                    'stock_id': tds[0].text,
                    'stock_name': tds[1].text,
                    'enabled': True,
                    'listed': False,
                }
                result.append(temp)

            return result
        except Exception as e:
            print('fail request stock ids, error:{e}')
