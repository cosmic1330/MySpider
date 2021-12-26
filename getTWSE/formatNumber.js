const fs = require("fs");
let twseTempJsonData = fs.readFileSync("./datas/TWSE/data.json");
let twseTempData = JSON.parse(twseTempJsonData);
let stocks = Object.keys(twseTempData);
let temp = {};
stocks.forEach((stock) => {
  let items = twseTempData[stock];
  items = items.map((item) => {
    return { ...item, t: parseInt(item.t) };
  });
  temp[stock] = items;
});

fs.writeFile(
  "datas/TWSE/toBackTest.json",
  JSON.stringify(temp),
  function (error) {
    if (error) {
      console.log("文件寫入失敗");
    } else {
      console.log("toBackTest.json寫入成功，你可以使用此資料進行回測");
    }
  }
);
