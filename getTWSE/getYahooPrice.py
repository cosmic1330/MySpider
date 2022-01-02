import requests
import json
def yahooPrice(key):
    print(key)
    response = requests.get('https://tw.quote.finance.yahoo.net/quote/q?type=ta&perd=d&mkt=10&sym='+key+'&v=1&callback=').text.lstrip("(").rstrip(");")
    response = json.loads(response)
    data = {}
    for li in response["ta"]:
        t = str(li["t"])
        data[t] = {'o': li["o"], 'h': li["h"], 'l':li["l"], 'c': li["c"], 'v': li["v"]}
    return data
