# 這支程式是檢查getPrice/index.py取得資料的正確性
import sys
from utils.getLocalJSON import getLocalJSON

JsonData = getLocalJSON()
listData = JsonData['data']
listKeys = JsonData['keys']
breakKeys = sys.argv[1] if len(sys.argv)>1 else ''

tempList = {}
for key in listKeys:
    if(key==breakKeys):
        break
    tempList[key] = len(listData[key])

# 取的所有股票的資料長度並去除重複
lens = list(set(tempList.values()))

# 取得不符合長度的股票代號
arr = []
for key in tempList:
    if(tempList[key] == 0):
        arr.append(key)

print(
    '\n','所有資料長度:',lens,
    '\n','不符合的股票:',arr
)