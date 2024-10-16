# Python 爬蟲:

## 目錄
本包程式檔包含

- example: (停止支援 請使用 getTWSE)
  - 功能: 使用 Selenium 更新每日股票需要的資料

- project-stock-query-database:
  - 功能: 配合docker-telegraf-influx-grafana專案的docker container，將資料寫入postgresql 

- project-stock-query-json:
  - 功能: 使用 Request 取得證交所資料，並寫入json檔
  
  - getEPSData:
    - 功能: 使用 Request 取得 EPS 股票代號
    - 條件: 去年及今年 EPS 為正的股票

  - getTWSE:
    - 功能: 抓取證交所資料
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
      - skp5: 主力 5 日集中
---

### Project: example

#### Getting Started

你的資料夾中會需要 chromedriver.exe，你可以到 http://chromedriver.storage.googleapis.com/index.html 下載 (GoogleDrive 需下載與本地相同的版本)

符合以上條件後你就可以執行

```cmd
python getPrice/index.py
python getPrice/index.py -r
```
---

### Project: project-stock-query-database
#### Getting Started
```cmd
cd project-stock-query-database
python main.py
```

---
### Project: project-stock-query-json

#### Getting Started
```javascript
// 執行
cd project-stock-query-json
python getTWSE/index.py
node getTWSE/filter.js
node getTWSE/run.js

// 資料檢查
node getTWSE/checkDataContent.js

// vscode task
或者你可以執行task.json
ctrl+shift+B  (1-4)依序執行
```
#### Docker Image (暫不支援)

```cmd
docker build -t myspider .
docker run -p --name myspidercontainer 4000:9527 myspider
```
---

