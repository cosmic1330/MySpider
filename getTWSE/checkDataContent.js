const fs = require("fs");
let rawdata = fs.readFileSync("./datas/TWSE/data.json");
let jsonData = JSON.parse(rawdata);
let keys = Object.keys(jsonData)

let error = []
keys.forEach(key => {
    for (let i = 0; i < jsonData[key].length; i++) {
        const element = jsonData[key][i];
        if(
            !element.hasOwnProperty('stockAgentMainPower') ||
            !element.hasOwnProperty('c') ||
            !element.hasOwnProperty('v') ||
            !element.hasOwnProperty('o') ||
            !element.hasOwnProperty('l') ||
            !element.hasOwnProperty('h') ||
            !element.hasOwnProperty('skp5') ||
            !element.hasOwnProperty('sumForeignNoDealer') ||
            !element.hasOwnProperty('sumING')
        ){
            error.push(key)
            break;
        }
    }
});
console.log("錯誤資料",error)