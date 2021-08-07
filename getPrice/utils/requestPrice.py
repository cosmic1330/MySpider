import requests
import json
def requestPrice(key):
    response = requests.get('https://tw.quote.finance.yahoo.net/quote/q?type=ta&perd=d&mkt=10&sym='+key+'&v=1&callback=').text.lstrip("(").rstrip(");")
    response = json.loads(response)
    return response
