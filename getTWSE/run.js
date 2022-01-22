const fs = require("fs");
const { Ma } = require("@ch20026103/anysis");
let twseJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseData = JSON.parse(twseJsonData);

let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
let epsData = JSON.parse(epsJsonData).dataList;

let ma = new Ma();

/* bolling */
// let purchaseList = [];
// epsData.forEach((stockId) => {
//   let stockData = twseData[stockId];
//   if (!stockData) return;
//   stockData = ma.getBoll(stockData);

//   let length = stockData.length;
//   if (
//     (stockData[length - 1]["sumING"]>0 || stockData[length - 1]["sumForeignNoDealer"]>0) &&
//     stockData[length - 1]["bollLb"] < stockData[length - 1]["c"] &&
//     stockData[length - 2]["bollLb"] < stockData[length - 2]["c"] &&
//     (stockData[length - 3]["bollLb"] > stockData[length - 3]["c"] ||
//       stockData[length - 4]["bollLb"] > stockData[length - 4]["c"])
//   ) {
//     purchaseList.push({
//       date: stockData[length - 1]["t"],
//       price: stockData[length - 1]["c"],
//       ING: stockData[length - 1]["sumING"],
//       [stockId]: stockData[length - 1]["name"],
//     });
//   }
// });
// console.log(purchaseList);

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
    stockData[length - 3]["sumING"] > 10
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
