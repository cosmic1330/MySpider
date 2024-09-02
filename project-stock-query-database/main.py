import datetime
from loguru import logger
from middleware.proxy.utils.requestByProxy import requestByProxy
import os
import globals
from components.EpsModel import EpsModle
from components.StocksModel import StocksModel
from components.MonthlyRevenueModel import MonthlyRevenueModel
from components.DealDateModel import DealDateModel
from components.DailyDealModel import DailyDealModel
from components.LegalPersonModel import LegalPersonModel
from components.TaiexModel import TaiexModel
from middleware.orm.database import session
from middleware.orm.models import Stock
from components.LeaderModel import LeaderModel

if __name__ == '__main__':
    logger.add(
        f'{globals.EntryPoint}/logs/{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='ERROR'
    )
    
    # Stocks model
    stocks = StocksModel()
    
    # DealDate model
    dealDate = DealDateModel()
    if(dealDate.check_deal_date_count() == 0):
        dealDate.initial_deal_date()
    
    # DailyDeal model
    dailyDeal = DailyDealModel()
    if(dailyDeal.check_daily_deal_count() == 0):
        dailyDeal.initial_daily_deal()
    
    # LegalPerson model
    legalPerson = LegalPersonModel()
    if(legalPerson.check_legal_person_count() == 0):
        legalPerson.initial_legal_person()
        
    # Eps model
    eps = EpsModle()
    if(eps.check_eps_count() == 0):
        eps.initial_history_eps()
    
    # MonthlyRevenueModel model
    monthlyRevenue = MonthlyRevenueModel()
    if(monthlyRevenue.check_monthly_revenue_count() == 0):
        monthlyRevenue.initial_monthly_revenue()
        
    # Taiex model
    taiex = TaiexModel()
    if(taiex.check_taiex_count() == 0):
        taiex.initial_taiex()    
    
    # # Leader model
    # leader = LeaderModel()
    # if(leader.check_leader_count() == 0):
    #     leader.initial_leader()
     
    current_time = datetime.datetime.now()
    if datetime.datetime.today().weekday() in range(0, 4) and current_time.hour in range(9, 18):
        print('在交易時間內，不執行補資料動作')
    else:
        # dealDate.query_lose_data()
        dailyDeal.query_lose_data()
        # legalPerson.query_lose_data()
        # eps.query_lose_data()
        # monthlyRevenue.query_lose_data()
        # taiex.query_lose_data()
        
    # 工具函式
    """
    修正每日交易資料
    repair_daily_deal() 會以Yahoo API資料修正缺少的每日交易資料
    """
    # dailyDeal.repair_daily_deal()
    
    
    """
    刷新股票代號
    refresh_current_stockIds() 會將目前所有股票代號刷新存入資料庫
    """
    # stocks.refresh_current_stockIds()
    
    
    """
    取得proxy ip列表
    """
    # requestByProxy()
    
    session.close()