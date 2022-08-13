import requests 
from bs4 import BeautifulSoup

URL = "https://nmlegis.gov/Members/Legislator?SponCode=SBACA"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
#print(soup.prettify())

info = soup.find('div', attrs = {'class':'col-xs-12 col-sm-9 legislator-information'}) 
out_dict = dict()
for row in info.findAll('li', attrs = {'class':'list-group-item'}):
    attr = row.b.text
    attr = attr.replace(':', '')
    try: 
        datum = row.span.text
    except: 
        datum = row.a.text
    dict_add = {attr:datum}
    out_dict.update(dict_add)
print(out_dict)
