const fs = require("fs");
let rawdata = fs.readFileSync("./datas/TWSE/data.json");
let jsonData = JSON.parse(rawdata);
let keys = Object.keys(jsonData);

let arr = [];
keys.forEach((key) => {
  let stock = jsonData[key];
  let length = stock.length;
  if (
    stock[length - 1]["sumING"] > 100 &&
    stock[length - 2]["sumING"] > 100 &&
    stock[length - 3]["sumING"] > 0
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
