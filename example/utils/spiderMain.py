

from bs4 import BeautifulSoup
def spiderMain(key,driver):
   driver.get("https://www.wantgoo.com/stock/{}/major-investors/main-trend".format(key))
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
         stockAgentMainPower = tds[2].text
         skp5 = tds[4].text.replace('%', '')
         obj = {"stockAgentMainPower":int(stockAgentMainPower),"skp5":float(skp5)}
         data[t] = obj

   if(status==False):
      return spiderMain(key,driver)
   else:
      return data
