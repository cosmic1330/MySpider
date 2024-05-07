import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import loguru
import requests
import execjs
import re
from bs4 import BeautifulSoup

def getProxiesFromProxyNova():
    proxies = []
    # 配置 Chrome 選項
    chrome_options  = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 啟用無頭模式
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    # 按照網站規則使用各國代碼傳入網址取得各國 IP 代理
    countries = [
        'tw',
        'jp',
        'kr',
        'id',
        'my',
        'th',
        'vn',
        'ph',
        'hk',
        'us'
    ]
    for country in countries:
        url = f'https://www.proxynova.com/proxy-server-list/country-{country}/'
        loguru.logger.debug(f'getProxiesFromProxyNova: {url}')
        
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        
        # response = requests.get(url)
        # loguru.logger.warning(f'getProxiesFromProxyNova: {country} requesting...')
        # if response.status_code != 200:
        #     loguru.logger.debug(f'getProxiesFromProxyNova: status code is not 200')
        #     continue
        # html = response.text
        
        loguru.logger.success(f'getProxiesFromProxyNova: {country} html downloaded.')
        soup = BeautifulSoup(html,"html.parser")
        # 取得id為tbl_proxy_list的table
        table = soup.find('table', id='tbl_proxy_list')
        rows = table.find('tbody').find_all('tr')
        loguru.logger.warning(f'getProxiesFromProxyNova: {country} table scanning ...')
        for row in rows:
            tds = row.find_all('td')
            # 沒有內容就跳過
            if len(tds) == 1:
                continue
            
            abbr = tds[0].select_one('abbr')
            if(abbr):
                ip = abbr.text.strip()
            else:
                ip = tds[0].text.strip()
            # 取出 Port 欄位值
            port = tds[1].text.strip()
            # 組合 IP 代理
            proxy = f'{ip}:{port}'
            proxies.append(proxy)
        loguru.logger.success(f'getProxiesFromProxyNova: scanned.')
        loguru.logger.debug(f'getProxiesFromProxyNova: {len(proxies)} proxies is found.')
        # 每取得一個國家代理清單就休息一秒，避免頻繁存取導致代理清單網站封鎖
        time.sleep(1)
    driver.quit()
    return proxies
