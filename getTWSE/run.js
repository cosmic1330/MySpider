const fs = require("fs");
let twseJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseData = JSON.parse(twseJsonData);

let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
let epsData = JSON.parse(epsJsonData).dataList;

let purchaseList = [];
epsData.forEach((stockId) => {
  let stockData = twseData[stockId];
  if (!stockData) return;

  let length = stockData.length;
  if (
    stockData[length - 1]["sumING"] > 100 &&
    stockData[length - 2]["sumING"] > 100 &&
    stockData[length - 3]["sumING"] > 100
  ) {
    purchaseList.push({
      date: stockData[length - 1]["t"],
      price: stockData[length - 1]["c"],
      ING: stockData[length - 1]["sumING"],
      [stockId]: stockData[length - 1]["name"],
    });
  }
});
console.log(purchaseList);
