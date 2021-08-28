from getLocalJSON import getLocalJSON
from getYahooPrice import yahooPrice
from getING import getING
import json
import sys
import random
import time


try:
    # 1.取得本地檔案資料
    JsonData = getLocalJSON()
    listData = JsonData['data']
    stocks = JsonData['keys']

    # 2.列出local缺少的資料 和 缺少的日期
    missDates = []
    temp = {}
    change = []
    for stock in stocks:
        temp[stock] = {}
        yahooData = yahooPrice(stock)
        dates = yahooData.keys()
        for date in dates:
            if(date not in listData[stock]):
                change.append(stock)
                missDates.append(date)
                temp[stock][date] = yahooData[date]
    unique_set = set(missDates)
    missDates = list(unique_set)

    # 3.取得TWSE的法人資料
    for miss in missDates:
        timer = random.randint(1,5)
        time.sleep(timer)
        ingData = getING(miss)
        for stock in temp.keys():
            if(miss in temp[stock]):
                if(stock in ingData):
                    temp[stock][miss] = {**temp[stock][miss], **ingData[stock]}
                    listData[stock][miss] = temp[stock][miss]

    
    # 4.整新更新後的數據
    j = json.dumps(listData)
    f = open("./datas/TWSE/datatemp.json", 'w', encoding='UTF-8')
    f.write(j)
    f.close()
    print('Step not finish, Please run `node getTWSE/filter.js`')
except:
    print("Fail")
    # driver.close()
