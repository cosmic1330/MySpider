import requests
import json


def getING(date):
  url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={date}&selectType=ALLBUT0999&response=json"
  response = requests.get(url).text
  response = json.loads(response)
  data = {}
  for li in response["data"]:
    # 外資買賣超(張)
    foreign = li[4].replace(",", "")
    foreign = int(foreign) / 1000
    foreign = round(foreign)
    # 投信買賣超(張)
    ing = li[10].replace(",", "")
    ing = int(ing) / 1000
    ing = round(ing)
    data[li[0]] = {"sumING": ing, "sumForeignNoDealer": foreign,
                   "skp5": 0, "stockAgentMainPower": 0}
  return data
