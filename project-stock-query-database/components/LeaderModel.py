from middleware.orm.models import Leader, Stock, DealDate
from middleware.orm.database import session
from datetime import datetime
from utils.delay import delay
import loguru
import requests
import json
from decimal import Decimal
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LeaderModel:
    def __init__(self):
        pass

    def query_lose_data(self):
        pass

    # query loss date from twse

    def check_leader_count(self):
        return session.query(Leader).count()

    def initial_leader(self):
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        new_data = self.queryWantgooData(2330, stocks[0].stock_name)
        print(new_data)

    @classmethod
    def queryWantgooData(self, stock_id, stock_name, start_date=None, end_date=None):
        # 配置 Chrome 選項
        chrome_options  = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # 啟用無頭模式
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://www.wantgoo.com/stock/{stock_id}/major-investors/main-trend#main-trend"
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            table = soup.find('table')
            tbody = table.find('tbody')
            return tbody
        except Exception as e:
            print(f'fail request {stock_id} yahoo data', e)
