const fs = require("fs");
const { Ma, Williams, Macd } = require("@ch20026103/anysis");
let twseJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseData = JSON.parse(twseJsonData);

let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
let epsData = JSON.parse(epsJsonData).dataList;

let ma = new Ma();
let williams = new Williams();
let macd = new Macd();

/* k sell */
let purchaseList2 = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  let williamsData = williams.getAllWillams(stockData);

  let length = stockData.length;
  if (
    stockData[length - 1]["v"] > 1000 &&
    stockData[length - 1]["h"] < stockData[length - 2]["h"] &&
    stockData[length - 1]["l"] < stockData[length - 2]["l"] &&
    (williamsData[williamsData.length - 2].williams9 > -10 ||
      williamsData[williamsData.length - 3].williams9 > -10) &&
    (williamsData[williamsData.length - 2].williams18 > -10 ||
      williamsData[williamsData.length - 3].williams18 > -10)
  ) {
    purchaseList2.push({
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      I: stockData[length - 1]["sumING"],
      [stockId]: stockData[length - 1]["name"],
      F: stockData[length - 1]["sumForeignNoDealer"],
    });
  }
});
console.log(
  "Method: K線反轉(賣)\n",
  "----------------------------\n",
  purchaseList2,
  "\n",
  "----------------------------\n"
);

/* k buy */
let purchaseList1 = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  let ma10Data = ma.getMa10(stockData.slice(-11));
  let williamsData = williams.getAllWillams(stockData);

  let length = stockData.length;
  if (
    stockData[length - 1]["v"] > 1000 &&
    stockData[length - 1]["h"] > stockData[length - 2]["h"] &&
    stockData[length - 1]["l"] > stockData[length - 2]["l"] &&
    (williamsData[williamsData.length - 2].williams9 < -80 ||
      williamsData[williamsData.length - 3].williams9 < -80) &&
    (williamsData[williamsData.length - 2].williams18 < -80 ||
      williamsData[williamsData.length - 3].williams18 < -80) &&
    stockData[length - 1]["c"] > ma10Data[ma10Data.length - 1]["ma10"]
  ) {
    purchaseList1.push({
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      I: stockData[length - 1]["sumING"],
      [stockId]: stockData[length - 1]["name"],
      F: stockData[length - 1]["sumForeignNoDealer"],
    });
  }
});
console.log(
  "Method: K線反轉(買)\n",
  "----------------------------\n",
  purchaseList1,
  "\n",
  "----------------------------\n"
);


/* macd buy */
let purchaseList3 = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  const Ema26 = macd.getEMA26(stockData);
  const Ema12 = macd.getEMA12(stockData);
  const Dif = macd.getDIF(stockData, Ema12, Ema26);
  const Macd9 = macd.getMACD9(stockData, Dif)
  
  let ma10Data = ma.getMa10(stockData.slice(-11));
  let ma5Data = ma.getMa5(stockData.slice(-6));
  let ma20Data = ma.getMa20(stockData.slice(-21));
  let length = stockData.length;
  if (
    Macd9[length - 1]["OSC"] > 0 &&
    Macd9[length - 1]["OSC"] > Macd9[length - 2]["OSC"] &&
    (Macd9[length - 3]["OSC"] < 0 || Macd9[length - 4]["OSC"] < 0 ) &&
    stockData[length - 1]["c"] > ma10Data[ma10Data.length - 1]["ma10"] &&
    ma5Data[ma5Data.length - 1]["ma5"] > ma10Data[ma10Data.length - 1]["ma10"] &&
    ma5Data[ma5Data.length - 1]["ma5"] > ma20Data[ma20Data.length - 1]["ma20"]
  ) {
    purchaseList3.push({
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      I: stockData[length - 1]["sumING"],
      [stockId]: stockData[length - 1]["name"],
      F: stockData[length - 1]["sumForeignNoDealer"],
    });
  }
});
console.log(
  "Method: Macd反轉(買)\n",
  "----------------------------\n",
  purchaseList3,
  "\n",
  "----------------------------\n"
);

/* stock */
let purchaseList = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;

  stockData = ma.getMa10(stockData);
  let length = stockData.length;
  if (
    stockData[length - 1]["v"] > 1000 &&
    stockData[length - 1]["sumING"] > 100 &&
    stockData[length - 2]["sumING"] > 100 &&
    stockData[length - 3]["sumING"] > 100
  ) {
    purchaseList.push({
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      I: stockData[length - 1]["sumING"],
      F: stockData[length - 1]["sumForeignNoDealer"],
      [stockId]: stockData[length - 1]["name"],
    });
  }
});
console.log(
  "Method: 投信買進(正)\n",
  "----------------------------\n",
  purchaseList,
  "\n",
  "----------------------------\n"
);


