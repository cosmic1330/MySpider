const fs = require("fs");
const dotenv = require("dotenv");
const envConfig = dotenv.parse(fs.readFileSync(".env.local"));
const MongoClient = require("mongodb").MongoClient;

// save file

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
  "datas/TWSE/toMongodb.json",
  JSON.stringify(temp),
  function (error) {
    if (error) {
      console.log("文件寫入失敗");
    } else {
      console.log("toMongodb.json寫入成功，你可以使用此資料進行回測");
    }
  }
);

// save db

let epsJsonData = fs.readFileSync("./datas/Eps/data.json");
let epsData = JSON.parse(epsJsonData).dataList;

for (const k in envConfig) {
  process.env[k] = envConfig[k];
}

const MONGODB_URI = process.env.MONGODB_URI;
const MONGODB_DB = process.env.MONGODB_DB;

MongoClient.connect(MONGODB_URI, function (err, client) {
  if (err) throw err;
  console.log("mongodb is running!");
  const db = client.db(MONGODB_DB);

  epsData.forEach(
    (i) => {
      if (Object.hasOwnProperty.call(temp, i)) {
        const element = temp[i];

        // delete data
        db.collection(i)
          .deleteMany({})
          .then((res) => console.log({ ...res, id: i }));

        // if no collection
        // db.createCollection(i);

        // insert data
        db.collection(i)
          .insertMany(element)
          .then((res) =>
            console.log({
              acknowledged: res.acknowledged,
              insertedCount: res.insertedCount,
              id: i,
            })
          );
      }
    }

    // db.collection("1101")
    //   .find()
    //   .sort({ metacritic: -1 })
    //   .limit(20)
    //   .toArray()
    //   .then((res) => {
    //     console.log(res);
    //     client.close();
    //   });
  );
});
