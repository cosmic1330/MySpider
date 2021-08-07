import requests
from bs4 import BeautifulSoup
from utils.getEps import getSeasonEps
from utils.checkKey import dicCheckKey
import json

""" 爬蟲：這今年即去年eps """
# 連線
r = requests.get("https://www.cnyes.com/twstock/financial4.aspx") #將此頁面的HTML GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser

# 取得所有季選項
options = soup.select('select[name="ctl00$ContentPlaceHolder1$D3"] option')

# 建立字典
response = getSeasonEps(options[0].text)
dic={x[0]:[] for x in response}

# 取的最新季及去年eps資料
i = 0
now = options[i].text
nowSeason = now[5:]
before = options[i+int(nowSeason)].text

for season in [now,before]:
    items = getSeasonEps(season)
    for item in items:
        if(dicCheckKey(item[0],dic)):
            dic[item[0]].append(item[7])

# 挑選目前及去年eps為正的股票
response = {"season":[now,before],"check":dic, "dataList":[] }
for stock in dic:
    if(float(dic[stock][0]) > 0 and float(dic[stock][1]) > 0):
        response["dataList"].append(stock)

# 寫入json
j = json.dumps(response)
f = open("./datas/Eps/data.json", 'w', encoding='UTF-8')
f.write(j)
f.close()

print(j)
