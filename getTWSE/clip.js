const fs = require("fs");
const dotenv = require("dotenv");
const envConfig = dotenv.parse(fs.readFileSync(".env.local"));
const MongoClient = require("mongodb").MongoClient;

// save file
let twseTempJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseTempData = JSON.parse(twseTempJsonData);
let stocks = Object.keys(twseTempData);
let stock = 9904;
let temp = [];
twseTempData[stock].forEach((element) => {
  temp.push({
    o: 26.4,
    l: element.l,
    h: element.h,
    c: element.c,
    v: element.v,
    t: parseInt(element.t),
  });
});

fs.writeFile(
  "datas/TWSE/clip.json",
  JSON.stringify(temp),
  function (error) {
    if (error) {
      console.log("文件寫入失敗");
    } else {
      console.log("toMongodb.json寫入成功，你可以使用此資料進行回測");
    }
  }
);
