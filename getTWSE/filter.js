const fs = require("fs");
let twseTempJsonData = fs.readFileSync("./datas/TWSE/datatemp.json");
let twseTempData = JSON.parse(twseTempJsonData);
let stocks = Object.keys(twseTempData);
let temp = {};
stocks.forEach((stock) => {
  let dates = Object.keys(twseTempData[stock]).sort().reverse();
  dates.splice(0, 1);
  dates = dates.reverse();
  let list = [];
  dates.forEach((date) => {
    let obj = {
      ...twseTempData[stock][date],
      name: twseTempData[stock]["name"],
      t: date,
    };
    list.push(obj);
  });
  temp[stock] = list;
});

fs.writeFile("datas/TWSE/data.json", JSON.stringify(temp), function (error) {
  if (error) {
    console.log("文件寫入失敗");
  } else {
    fs.unlink("datas/TWSE/datatemp.json", () =>
      console.log("寫入成功，你可以將data.json進行資料轉換")
    );
  }
});
