const fs = require("fs");
let rawdata = fs.readFileSync("./datas/TWSE/data.json");
let jsonData = JSON.parse(rawdata);

let rawdata2 = fs.readFileSync("./datas/Eps/data.json");
let keys = JSON.parse(rawdata2).dataList;

let arr = [];
keys.forEach((key) => {
  let stock = jsonData[key];
  if(!stock) return;
  let length = stock.length;
  if (
    stock[length - 1]["sumING"] > 100 &&
    stock[length - 2]["sumING"] > 100 &&
    stock[length - 3]["sumING"] > 100
  ) {
    arr.push({
      stock: key,
      date: stock[length - 1]["t"],
      name: stock[length - 1]["name"],
      price: stock[length - 1]["c"],
    });
  }
});
console.log(arr);
