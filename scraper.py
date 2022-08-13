import requests 
from bs4 import BeautifulSoup
import pandas as pd

for office, office_name in zip(['R', 'S'], ['House', 'Senate']):
    senate_url = f'https://nmlegis.gov/Members/Legislator_List?T={office}'
    r_senate = requests.get(senate_url)
    senate_soup = BeautifulSoup(r_senate.content, 'html5lib')
    office = senate_soup.find('a', attrs = {'id':'siteMapBreadcrumbs_lnkPage_2'})
    #print(office.text)
    senate_list = senate_soup.find('select', attrs = {'id':'MainContent_ddlLegislators'})
    rep_names = []
    rep_tags = []
    for rep in senate_list.findAll('option'):
         rep_tags.append(rep['value'])
         rep_names.append(rep.text)
    #    print(rep['value'])
    rep_names.pop(0)
    rep_tags.pop(0)
    #print(rep_names)

    dictlist = []
    for name, rep in zip(rep_names, rep_tags):
        URL = f"https://nmlegis.gov/Members/Legislator?SponCode={rep}"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        #print(soup.prettify())
        full_name = soup.find('span', attrs = {'id':'MainContent_formViewLegislatorName_lblLegislatorName'})
        party = full_name.text[(full_name.text.find('(') + 1):full_name.text.find(')')]
        info = soup.find('div', attrs = {'class':'col-xs-12 col-sm-9 legislator-information'}) 
        out_dict = {'Legislator':name, 'Party':party, 'Office':office.text}
        for row in info.findAll('li', attrs = {'class':'list-group-item'}):
            attr = row.b.text
            attr = attr.replace(':', '')
            try: 
                datum = row.span.text
            except: 
                try: 
                    datum = row.a.text
                except: 
                    datum = ''
            dict_add = {attr:datum}
            out_dict.update(dict_add)
        #print(out_dict)
        dictlist.append(out_dict)

    #print(dictlist)
    df = pd.DataFrame(dictlist)
    print(df)
    df.to_csv(f'NM_{office_name}_legislator_info.csv', index = False)
