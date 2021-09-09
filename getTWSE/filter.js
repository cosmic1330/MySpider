const fs = require("fs");
let rawdata = fs.readFileSync("./datas/TWSE/datatemp.json");
let jsonData = JSON.parse(rawdata);
let keys = Object.keys(jsonData);
let temp = {};
keys.forEach((key) => {
  let dates = Object.keys(jsonData[key]).sort().reverse();
  dates.splice(0, 1);
  dates = dates.reverse();
  let list = [];
  dates.forEach((date) => {
    let obj = { ...jsonData[key][date], name: jsonData[key]["name"], t: date };
    list.push(obj);
  });
  temp[key] = list;
});

fs.writeFile(
    "datas/TWSE/data.json",
    JSON.stringify(temp),
    function (error) {
      if (error) {
        console.log("文件寫入失敗");
      } else {
        fs.unlink("datas/TWSE/datatemp.json",()=> console.log("寫入成功，你可以將data.json進行處理"));
       
      }
    }
  );