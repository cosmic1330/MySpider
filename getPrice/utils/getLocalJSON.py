import json
import os
def getLocalJSON():
    file = './datas/Price/data.json'
    d = dict()
    with open(file, 'r', encoding="utf8") as obj:
        d['data'] = json.load(obj)
        d['keys'] = []
        for key in d['data']:
             d['keys'].append(key)
    return d