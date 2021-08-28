import json
def getLocalJSON():
    file = './datas/TWSE/data.json'
    d = dict()
    with open(file, 'r', encoding="utf8") as obj:
        jsonData = json.load(obj)
        d['data'] = {}
        d['keys'] = []
        for key in jsonData:
            d['keys'].append(key)
            d['data'][key] = {}
            for li in jsonData[key]:
                t = li['t']
                d['data'][key]["name"] = li["name"]
                d['data'][key][t] = {
                    'o':li['o'],
                    'l':li['l'],
                    "h":li['h'],
                    "c":li['c'],
                    "v":li['v'],
                    "skp5":li["skp5"],
                    "stockAgentMainPower":li["stockAgentMainPower"],
                    "sumING":li["sumING"],
                    "sumForeignNoDealer":li["sumForeignNoDealer"],
                }
                
    return d