import requests
from bs4 import BeautifulSoup
from getEPSData.utils.getEps import getSeasonEps
import json

# 建立Price/data.json
r = requests.get("https://www.cnyes.com/twstock/financial4.aspx") #將此頁面的HTML GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
options = soup.select('select[name="ctl00$ContentPlaceHolder1$D3"] option')
response = getSeasonEps(options[0].text)
dic={x[0]:[] for x in response}
j = json.dumps(dic)
f = open("./datas/Price/data.json", 'w', encoding='UTF-8')
f.write(j)
f.close()

# 建立EPS/data.json
dic2 = {"season":[],"check":{}, "dataList":[] }
j = json.dumps(dic2)
f = open("./datas/Eps/data.json", 'w', encoding='UTF-8')
f.write(j)
f.close()
