from middleware.orm.models import MonthlyRevenue, Stock
from bs4 import BeautifulSoup
from utils.delay import delay
from utils.isdecimal import isdecimal
from middleware.orm.database import session
from sqlalchemy.sql import select, label
from sqlalchemy import text, func
from datetime import datetime
import requests
import loguru
from decimal import Decimal


class MonthlyRevenueModel:
    def __init__(self):
        pass

    def check_database_year_month(self):
        return session.query(MonthlyRevenue.year, MonthlyRevenue.month).order_by(MonthlyRevenue.year.desc(), MonthlyRevenue.month.desc()).group_by(MonthlyRevenue.year, MonthlyRevenue.month).all()

    def query_lose_data(self):
        stocks = session.query(Stock.stock_id, Stock.stock_name).filter(
            Stock.enabled == True).all()
        for (stock_id, stock_name) in stocks:
            print(f"取得{stock_id} {stock_name}缺少的營收資料")
            try:
                # 取得最新資料
                r = requests.get(
                    f'https://tw.stock.yahoo.com/quote/{stock_id}.TW/revenue')
                # 將網頁資料以html.parser
                soup = BeautifulSoup(r.text, "html.parser")
                ul = soup.find('ul', class_="List(n)")
                lis = soup.find('ul', class_="List(n)")
                temp = {}
                for index, li in enumerate(lis):
                    try:
                        if (temp):
                            session.add(MonthlyRevenue(
                                year=temp['year'],
                                month=temp['month'],
                                stock_id=stock_id,
                                current_month_revenue=temp['current_month_revenue'],
                                previous_month_revenue=int(li.find('div').find_all('li')[
                                    0].text.replace(',', '')),
                                previous_year_same_month_revenue=temp['previous_year_same_month_revenue'],
                                month_over_month_revenue=Decimal(
                                    temp['month_over_month_revenue']),
                                year_over_year_revenue=Decimal(
                                    temp['year_over_year_revenue']),
                                current_year_cumulative_revenue=temp['current_year_cumulative_revenue'],
                                previous_year_cumulative_revenue=temp['previous_year_cumulative_revenue'],
                                compare_cumulative_revenue=Decimal(
                                    temp['compare_cumulative_revenue'])
                            ))
                            session.commit()
                            loguru.logger.success(
                                f'[Success] create {stock_id} {year}/{month} monthly revenue data')
                    except Exception as e:
                        session.rollback()  # 回滾交易以清除未提交的更改
                        loguru.logger.warning(
                            f"[Skip] stockid:{stock_id} monthly_data:{year}/{month}")
                        break
                    year, month = li.find('div').find('div').text.split('/')
                    temp = {
                        'year': year,
                        'month': month,
                        'current_month_revenue': int(li.find('div').find_all('li')[
                            0].text.replace(',', '')),
                        'previous_year_same_month_revenue': int(
                            li.find('div').find_all('li')[2].text.replace(',', '')),
                        'month_over_month_revenue':  round(
                            float(li.find('div').find_all('li')[1].text.replace(',', '').strip('%')), 2),
                        'year_over_year_revenue': round(
                            float(li.find('div').find_all('li')[3].text.replace(',', '').strip('%')), 2),
                        'current_year_cumulative_revenue': int(
                            li.find('div').find_all('li')[4].text.replace(',', '')),
                        'previous_year_cumulative_revenue': int(
                            li.find('div').find_all('li')[5].text.replace(',', '')),
                        'compare_cumulative_revenue': round(
                            float(li.find('div').find_all('li')[6].text.replace(',', '').strip('%')), 2)
                    }
            except Exception as e:
                loguru.logger.error(
                    f'[Fail] create {stock_id} monthly revenue data', e)
                print(e)

    def query_lose_data_twse(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        year = 2010
        month = 1

        db_year_month = self.check_database_year_month()
        print("資料庫年月份:", db_year_month)

        # 刷新上個月資料
        try:
            session.query(MonthlyRevenue).filter(
                MonthlyRevenue.year == current_year, MonthlyRevenue.month == current_month).delete()

            # 寫入資料庫
            session.commit()
            loguru.logger.success(
                'Success delete last month Monthly Revenue data')
        except Exception as e:
            # 發生例外錯誤，還原交易
            session.rollback()
            loguru.logger.error('Fail delete last month Monthly Revenue data')

        # 所有可能的年月組合
        before_combinations = [(year, month) for year in range(
            current_year-1-1911, year-1911, -1) for month in range(1, 13)]
        current_combinations = [(year, month) for year in range(
            current_year-1911, current_year-1911+1) for month in range(1, current_month+1)]
        all_combinations = before_combinations + current_combinations
        # 找出缺少的年月組合
        missing_combinations = [
            comb for comb in all_combinations if comb not in db_year_month]
        print("缺少的年月組合：", missing_combinations)

        for year, month in missing_combinations:
            print(f"取得{year}年{month}月資料")
            new_data = self.queryData(year, month)
            for data in new_data:
                try:
                    session.add(data)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    loguru.logger.error(
                        f'Fail create {data.stock_id} {year}/{month} monthly revenue data', e)

            loguru.logger.success(
                f'Success create {year}/{month} monthly revenue data')
            delay()
        loguru.logger.info(f"Query monthly_revenue is done.")

    def check_monthly_revenue_count(self):
        return session.query(MonthlyRevenue).count()

    def initial_monthly_revenue(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        year = 2010
        month = 1

        print(f"取得2010年1月-{current_year}年{current_month}月營收資料")

        while year < current_year or month < current_month:
            print(f"取得{year}年{month}月資料")
            new_data = self.queryDataTwse(year-1911, month)

            for data in new_data:
                try:
                    session.add(data)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    loguru.logger.error(
                        f'Fail create {data.stock_id} {year}/{month} monthly revenue data', e)

            loguru.logger.success(
                f'Success create {year}/{month} monthly revenue data')
            month += 1
            if month > 12:
                year += 1
                month = 1
            delay()
        loguru.logger.info(f"Initial monthly_revenue is done.")

    @classmethod
    def queryDataTwse(self, year, month):
        try:
            # 連線
            headers = {
                'Content-Type': 'text/html; charset=utf-8'
            }
            r = requests.get(
                f"https://mops.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}_0.html", headers=headers)
            page0_soup = BeautifulSoup(
                r.text, "html.parser")  # 將網頁資料以html.parser
            delay()
            # 沒有資料就直接結束---------------
            page0_data = self.getSoupData(page0_soup, year, month)
            if (len(page0_data) == 0):
                return []
            # -------------------------------

            r = requests.get(
                f"https://mops.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}_1.html", headers=headers)
            page1_soup = BeautifulSoup(
                r.text, "html.parser")  # 將網頁資料以html.parser
            page1_data = self.getSoupData(page1_soup, year, month)
            return page0_data+page1_data
        except Exception as e:
            loguru.logger.error(f'Fail query {year}/{month} data')
            raise
            print(e)

    @staticmethod
    def getSoupData(soup, year, month):
        # 取得所有資料
        temp = []
        arr = []
        td_elements = soup.find_all('td', colspan="2")
        for td_element in td_elements:
            inner_table = td_element.find('table')
            if inner_table is not None:
                data_rows = inner_table.find_all('tr', align='right')
                for data_row in data_rows:
                    if data_row.find('td').get('align') == 'center' and data_row.find('td').text != '11':
                        td_elements = data_row.find_all('td')
                        td_texts = []
                        for td in td_elements[:10]:
                            td_texts.append(td.text.strip().replace(',', ''))

                        # td_texts = [
                            # 股票代號
                            # 股票名稱
                            # 當月營收
                            # 上月營收
                            # 去年當月營收
                            # 上月比較增減(%)
                            # 去年同月增減(%)
                            # 今年累計到本月營收
                            # 去年累計到本月營收
                            # 前期比較增減(%)
                        # ]
                        # 使用切片操作去掉股票名稱但保留股票代號
                        #

                        if (td_texts[0] not in temp):
                            temp.append(td_texts[0])
                            arr.append(MonthlyRevenue(
                                year=int(year) + 1911,  # 將民國年轉換為西元年
                                month=month,
                                stock_id=td_texts[0],
                                current_month_revenue=int(td_texts[2].replace(
                                    ',', '')) if td_texts[2].replace(',', '').isdigit() else 0,
                                previous_month_revenue=int(td_texts[3].replace(
                                    ',', '')) if td_texts[3].replace(',', '').isdigit() else 0,
                                previous_year_same_month_revenue=int(td_texts[4].replace(
                                    ',', '')) if td_texts[4].replace(',', '').isdigit() else 0,
                                month_over_month_revenue=Decimal(td_texts[5]) if isdecimal(
                                    td_texts[5]) else Decimal('0.00'),
                                year_over_year_revenue=Decimal(td_texts[6]) if isdecimal(
                                    td_texts[6]) else Decimal('0.00'),
                                current_year_cumulative_revenue=int(td_texts[7].replace(
                                    ',', '')) if td_texts[7].replace(',', '').isdigit() else 0,
                                previous_year_cumulative_revenue=int(td_texts[8].replace(
                                    ',', '')) if td_texts[8].replace(',', '').isdigit() else 0,
                                compare_cumulative_revenue=Decimal(td_texts[9]) if isdecimal(
                                    td_texts[9]) else Decimal('0.00')
                            ))
        return arr
