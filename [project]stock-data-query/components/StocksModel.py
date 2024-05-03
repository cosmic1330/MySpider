import requests
from middleware.orm.models import Stock
from middleware.orm.database import session

import loguru

class StocksModel:
    def __init__(self):
        pass
    
    def check_stockid_count(self):
        return session.query(Stock).count()
        
    def initial_current_stockIds(self):
        # get database stock ids
        try:
            ids = session.query(Stock).all()
            session.query(Stock).update({Stock.enabled: False})
            session.commit()
        except Exception as e:
            session.rollback()
            loguru.logger.error('Fail update stock disabled')
            print(e)
        
        # create new stock ids
        datas = self.getStockIds()
        for data in datas:
            new_stock = Stock(
                stock_id=data['stock_id'], 
                stock_name=data['stock_name'], 
                enabled=data['enabled']
            )
            try:
                session.add(new_stock)
                session.commit()
            except Exception as e:
                session.rollback()
                try:
                    session.query(Stock).filter(Stock.stock_id == data['stock_id']).update({Stock.enabled: True})
                    session.commit()
                except Exception as e:
                    session.rollback()
                    loguru.logger.error('Fail create stock id')
                    print(e)
        
        loguru.logger.info(f"stocks id update is done.")
    
    @staticmethod
    def getStockIds():
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?response=json&_=1688900750130"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()['data']
            result = [{
                'stock_id': item[0], 
                'stock_name': item[1], 
                'enabled': True,
            } for item in data]

            
            return result
        except Exception as e:
            print('fail request stock ids')
            print(e)