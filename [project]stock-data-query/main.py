import datetime
from loguru import logger
from middleware.proxy.utils.requestByProxy import requestByProxy
import os
import globals
from components.EpsModel import EpsModle
from components.StocksModel import StocksModel
from components.MonthlyRevenueModle import MonthlyRevenueModle
from middleware.orm.database import session
from middleware.orm.models import Stock

if __name__ == '__main__':
    logger.add(
        f'{globals.EntryPoint}/logs/{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # 使用proxy
    # requestByProxy()
    
    # 使用orm
    # stocks = session.query(Stock).all()
    # for stock in stocks:
    #     print(f"Stock name: {stock.stock_name}, Id: {stock.stock_id}")

    
    # Stocks model
    stocks = StocksModel()
    if(stocks.check_stockid_count() == 0):
        stocks.initial_current_stockIds()
        
    # Eps model
    eps = EpsModle()
    if(eps.check_eps_count() == 0):
        eps.initial_history_eps()
    eps.query_lose_data()
    
    # MonthlyRevenueModle model
    monthlyRevenue = MonthlyRevenueModle()
    if(monthlyRevenue.check_monthly_revenue_count() == 0):
        monthlyRevenue.initial_monthly_revenue()
    # monthlyRevenue.query_lose_data()
    
    session.close()