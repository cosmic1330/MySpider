const fs = require("fs");
const { Ma, Williams, Macd, Rsi } = require("@ch20026103/anysis");
let ma = new Ma();
let williams = new Williams();
let macd = new Macd();
let rsi = new Rsi();

const show = (func, name, today) => {
  let twseJsonData = fs.readFileSync("./datas/TWSE/data.json");
  let twseData = JSON.parse(twseJsonData);
  let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
  let epsData = JSON.parse(epsJsonData).dataList;

  const purchaseList = [];
  const errList = [];

  epsData.forEach((stockId) => {
    try {
      const data = func(twseData, stockId, today);
      if (data) purchaseList.push(data);
    } catch (error) {
      errList.push(stockId);
      return;
    }
  });

  console.log(
    `Method: ${name}\n`,
    "----------------------------\n",
    purchaseList,
    "\n",
    "----------------------------\n"
  );
  if (errList.length > 0) {
    console.log(
      `Error: ${name}\n`,
      "----------------------------\n",
      errList,
      "\n",
      "----------------------------\n"
    );
  }
};

/* k sell */
const k_sell = (twseData, stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  let williamsData = williams.getAllWillams(stockData);

  let length = stockData.length;
  if (
    stockData[length - 1]["v"] > 1000 &&
    stockData[length - 2]["v"] > 1000 &&
    stockData[length - 1]["h"] < stockData[length - 2]["h"] &&
    stockData[length - 1]["l"] < stockData[length - 2]["l"] &&
    (williamsData[williamsData.length - 2].williams9 > -10 ||
      williamsData[williamsData.length - 3].williams9 > -10) &&
    (williamsData[williamsData.length - 2].williams18 > -10 ||
      williamsData[williamsData.length - 3].williams18 > -10)
  ) {
    return {
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      I: stockData[length - 1]["sumING"],
      [stockId]: stockData[length - 1]["name"],
      F: stockData[length - 1]["sumForeignNoDealer"],
    };
  }
  return;
};

const k_buy = (twseData, stockId, today = 1) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  let ma10Data = ma.getMa10(stockData);
  let bollData = ma.getBoll(stockData);
  let williamsData = williams.getAllWillams(stockData);

  let length = stockData.length;
  if (
    stockData[length - today]["v"] > 1000 &&
    stockData[length - (today + 1)]["v"] > 1000 &&
    stockData[length - today]["h"] > stockData[length - (today + 1)]["h"] &&
    stockData[length - today]["l"] > stockData[length - (today + 1)]["l"] &&
    (williamsData[williamsData.length - (today + 1)].williams9 < -80 ||
      williamsData[williamsData.length - (today + 2)].williams9 < -80) &&
    (williamsData[williamsData.length - (today + 1)].williams18 < -80 ||
      williamsData[williamsData.length - (today + 2)].williams18 < -80) &&
    stockData[length - today]["c"] >
      ma10Data[ma10Data.length - today]["ma10"] &&
    ((stockData[length - today]["c"] >
      bollData[bollData.length - today]["ma25"] &&
      (stockData[length - (today + 1)]["c"] <
        bollData[bollData.length - (today + 1)]["ma25"] ||
        stockData[length - (today + 2)]["c"] <
          bollData[bollData.length - (today + 2)]["ma25"])) ||
      (stockData[length - today]["c"] >
        bollData[bollData.length - today]["ma25"] &&
        stockData[length - today]["c"] <
          bollData[bollData.length - today]["bollUb"]))
  ) {
    return {
      date: stockData[length - today]["t"],
      price: stockData[length - today]["c"],
      I: stockData[length - today]["sumING"],
      [stockId]: stockData[length - today]["name"],
      F: stockData[length - today]["sumForeignNoDealer"],
    };
  }
  return;
};

const macd_buy = (twseData, stockId, today = 1) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  const Ema26 = macd.getEMA26(stockData);
  const Ema12 = macd.getEMA12(stockData);
  const Dif = macd.getDIF(stockData, Ema12, Ema26);
  const Macd9 = macd.getMACD9(stockData, Dif);

  let ma10Data = ma.getMa10(stockData);
  let ma5Data = ma.getMa5(stockData);
  let ma20Data = ma.getMa20(stockData);
  let ma60Data = ma.getMa60(stockData);
  let rsiData = rsi.getAllRsi(stockData);
  let length = stockData.length;
  if (
    stockData[length - today]["v"] > 1000 &&
    stockData[length - (today + 1)]["v"] > 1000 &&
    Macd9[length - today]["OSC"] > 0 &&
    Dif[length - today]["DIF"] > Macd9[length - today]["MACD9"] &&
    Dif[length - (today + 1)]["DIF"] < Macd9[length - (today + 1)]["MACD9"] &&
    Macd9[length - today]["OSC"] > Macd9[length - (today + 1)]["OSC"] &&
    Macd9[length - today + 1]["OSC"] > Macd9[length - (today + 2)]["OSC"] &&
    Macd9[length - today + 2]["OSC"] > Macd9[length - (today + 3)]["OSC"] &&
    (Macd9[length - (today + 1)]["OSC"] < 0 ||
      Macd9[length - (today + 2)]["OSC"] < 0) &&
    stockData[length - today]["c"] >
      ma10Data[ma10Data.length - today]["ma10"] &&
    ma5Data[ma5Data.length - today]["ma5"] >
      ma20Data[ma20Data.length - today]["ma20"] &&
    ma20Data[ma20Data.length - today]["ma20"] >
      ma60Data[ma60Data.length - today]["ma60"] &&
    ma5Data[ma5Data.length - today]["ma5"] >
      ma60Data[ma60Data.length - today]["ma60"] &&
    rsiData[rsiData.length - today]["rsi6"]< 80 &&
    rsiData[rsiData.length - today]["rsi6"]> 50
  ) {
    return {
      date: stockData[length - today]["t"],
      price: stockData[length - today]["c"],
      I: stockData[length - today]["sumING"],
      [stockId]: stockData[length - today]["name"],
      F: stockData[length - today]["sumForeignNoDealer"],
    };
  }
};

const ing_buy = (twseData, stockId, today = 1) => {
  let stockData = twseData[stockId];
  if (!stockData) return;

  stockData = ma.getMa10(stockData);
  let length = stockData.length;
  if (
    stockData[length - today]["v"] > 1000 &&
    stockData[length - (today + 2)]["v"] > 1000 &&
    stockData[length - today]["sumING"] > 100 &&
    stockData[length - (today + 2)]["sumING"] > 100 &&
    stockData[length - (today + 3)]["sumING"] > 100
  ) {
    return {
      date: stockData[length - today]["t"],
      price: stockData[length - today]["c"],
      I: stockData[length - today]["sumING"],
      F: stockData[length - today]["sumForeignNoDealer"],
      [stockId]: stockData[length - today]["name"],
    };
  }
  return;
};

// show(k_sell, "K線反轉(賣)");
// show(k_buy, "K線反轉(買)",30);
show(macd_buy, "Macd反轉(買)", 33);
// show(ing_buy, "投信買進(買),50");
