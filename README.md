# Python爬蟲:
本包程式檔包含

- getEPSData: 
    - 功能: 使用Request取得EPS股票代號
    - 條件: 去年及今年EPS為正的股票
- getPrice:
    - 功能: 使用Selenium更新每日股票需要的資料
    - 條件: 包含
        - t: 交易日期
        - o: 開盤價
        - c: 收盤價
        - v: 交易量
        - h: 最高價
        - t: 最低價
        - sumForeignNoDealer: 外資購買張數
        - sumING: 投信購買張數
        - stockAgentMainPower: 主力購買張數
        - skp5: 主力5日集中

---

## Install
首先確定`datas/Price/data.json`及`datas/Eps/data.json`，如果不存在可以執行
```cmd
python initializeDataJSON.py
```
> 請先建立`datas/Price`及`datas/Eps`資料夾

---

## Program: getEPSData

### Getting Started
輸入以下command line後，程式會建立JSON檔在 `/datas/Eps/data.json`

```cmd
python getEPSData/index.py 
```
---

## Program: getPrice

### Getting Started
你的資料夾中會需要chromedriver.exe，你可以到 http://chromedriver.storage.googleapis.com/index.html 下載 (GoogleDrive需下載與本地相同的版本)

符合以上條件後你就可以執行
```cmd
python getPrice/index.py
python getPrice/index.py -r
```
> 你可能需要執行多次，因為Selenium不穩定

執行成功後您會看到 Fails 為空字串
```cmd
.....
Now stock:9945
Fails:[]
```

### Checking Data
取得JSON資料檔後可以run `getPrice/checkData.py`檢查資料長度是否相同，並列出不符合資的股票代號
```cmd
python ./getPrice/checkData.py
```

ex:
```cmd
 所有資料長度: [251, 244]
 不符合的股票: ['9802', '9902', '9904', '9905', '9907', '9908', '9910', '9911', '9914', '9917', '9919', '9921', '9924', '9925', '9927', '9930', '9933', '9934', '9935', '9938', '9939', '9940', '9941', '9942', '9943', '9944', '9945']
```

也可以設定要停止檢查的股票代號
ex: 
```cmd
檢查全部:
python .\getPrice\checkData.py

搜尋到1101:
python .\getPrice\checkData.py 1101
```

## Docker Image
```cmd
docker build -t myspider .
docker run -p --name myspidercontainer 4000:9527 myspider
```