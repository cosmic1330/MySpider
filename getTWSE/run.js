const fs = require("fs");
const { Ma, Williams } = require("@ch20026103/anysis");
let twseJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseData = JSON.parse(twseJsonData);

let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
let epsData = JSON.parse(epsJsonData).dataList;

let ma = new Ma();
let williams = new Williams();

/* bolling */
let purchaseList1 = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;
  let maData = ma.getMa10(stockData.slice(-11));
  let williamsData = williams.getAllWillams(stockData);

  let length = stockData.length;
  if (
    stockData[length - 1]["h"] > stockData[length - 2]["h"] &&
    stockData[length - 1]["l"] > stockData[length - 2]["l"] &&
    (williamsData[williamsData.length - 2].williams9 < -80 ||
      williamsData[williamsData.length - 3].williams9 < -80) &&
    (williamsData[williamsData.length - 2].williams18 < -80 ||
      williamsData[williamsData.length - 3].williams18 < -80) &&
    stockData[length - 1]["c"] > maData[maData.length - 1]["ma10"]
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
  "Method: K線反轉\n",
  "----------------------------\n",
  purchaseList1,
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
  "Method: 投信買進\n",
  "----------------------------\n",
  purchaseList,
  "\n",
  "----------------------------\n"
);

