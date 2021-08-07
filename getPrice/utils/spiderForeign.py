
from bs4 import BeautifulSoup
def spiderForeign(key,driver):
   driver.get("https://www.wantgoo.com/stock/{}/institutional-investors/trend".format(key))
   soup = BeautifulSoup(driver.page_source, 'html.parser')
   data = {}
   status = True
   rowsa = soup.find('table', 'table')
   rowsb = rowsa.tbody.find_all('tr')
   for row in rowsb:
      tds = row.find_all('td')
      if(tds[0].text==''):
         status = False
         break
      else:
         t = tds[0].text.replace('/', '')
         sumForeignNoDealer = tds[1].text.replace(',', '')
         sumING = tds[3].text.replace(',', '')
         obj = {"sumForeignNoDealer":int(sumForeignNoDealer),"sumING":int(sumING)}
         data[t] = obj

   if(status==False):
      return spiderForeign(key,driver)
   else:
      return data
