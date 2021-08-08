from selenium import webdriver
from utils.getLocalJSON import getLocalJSON
from utils.checkListKeys import checkListKeys
from utils.requestPrice import requestPrice
from utils.spiderMain import spiderMain
from utils.spiderForeign import spiderForeign
import json
import sys


# ---------------------------------------------------------------
def default(key, last):
    priceList = requestPrice(key)
    temp = []
    for li in reversed(priceList['ta']):
        if(str(li['t'])==str(last['t'])):
            break
        li['name'] = priceList['mem']['name']
        temp.append(li)
    temp = list(reversed(temp))
    return temp

# ---------------------------------------------------------------
##
#  I. 取得本地JOSN檔案並加入股價資料
##

# first.開啟Chrome drive
chrome_options  = webdriver.ChromeOptions()
chrome_options .add_argument('--headless')
driver = webdriver.Chrome()

try:
    # 1.取得本地檔案資料
    JsonData = getLocalJSON()
    listData = JsonData['data']
    listKeys = JsonData['keys']
    temps = {}
    fails = []
    if(len(sys.argv)>1):
        listKeys = reversed(listKeys)

    for key in listKeys:
        print('Now stock:'+key)
        last:object
        check:bool
        # 2.檢查股票最後一筆資料時間
        if(len(listData[key])>0):
            last = listData[key][-1]
            # 3.檢查最後一筆資料完整性
            check = checkListKeys(last,['o','h','l','c','v','name',"stockAgentMainPower","skp5","sumForeignNoDealer","sumING"])
        else:
            # 3.沒有資料則跳過檢查
            last = {'t':''}
            check = True

        # 4.最後一筆資料不完整不執行
        if(check==False):
            print(key+'最後一筆資料不完整，請檢查資料')
            break
        
        # 5.取得最後一筆資料時間之後的資料
        else:
            temp = default(key, last)
            temps[key] = temp

        # 6.如果沒有新資料則跳過此筆股票
        if(len(temps[key])<1):
            continue

    # ----------------------------------------------------------------
    ##
    #  II. 爬取主力資料並加入
    ##

        # 1.取得爬蟲主力資料
        table = spiderMain(key,driver)
        # 2.如果取得資料失敗則跳過此股票
        if(table==False):
            fails.append(key)
            continue
        else:
        # 3.依時間整合資料到temps
            for idx,li in enumerate(temps[key]):
                t= str(li["t"])
                if(checkListKeys(table,[t])):
                    temps[key][idx] = {**li, **table[t]}
                else:
                    obj= {"stockAgentMainPower":0,"skp5":0}
                    temps[key][idx] = {**li, **obj}


    # ----------------------------------------------------------------
    ##
    #  III. 爬取外資投信資料並加入
    ##

        # 1.取得爬蟲投信資料
        table = spiderForeign(key,driver)
        # 2.如果取得資料失敗則跳過此股票
        if(table==False):
            fails.append(key)
            continue
        else:
        # 3.依時間整合資料到temps
            for idx,li in enumerate(temps[key]):
                t= str(li["t"])
                if(checkListKeys(table,[t])):
                    temps[key][idx] = {**li, **table[t]}
                else:
                    obj= {"sumForeignNoDealer":0,"sumING":0}
                    temps[key][idx] = {**li, **obj}

    # ----------------------------------------------------------------
    ##
    #  IV. 整合資料
    ##
        listData[key].extend(temps[key])

    # ----------------------------------------------------------------
    ##
    #  V. 寫入json
    ##
        j = json.dumps(listData)
        f = open("./datas/Price/data.json", 'w', encoding='UTF-8')
        f.write(j)
        f.close()
        print('writed')

    driver.close()
    print('Fails:',fails,"\n")
except:
    driver.close()
