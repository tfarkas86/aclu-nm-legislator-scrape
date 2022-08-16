import requests 
from bs4 import BeautifulSoup
import pandas as pd
from os.path import basename
import re

# loop over offices, then navigate to pages for each legislator and scrape data
for office_identifier, office_name in zip(['R', 'S'], ['House', 'Senate']):
    
    print(office_name)
    office_url = f'https://nmlegis.gov/Members/Legislator_List?T={office_identifier}'
    r_office = requests.get(office_url)
    office_soup = BeautifulSoup(r_office.content, 'html5lib', from_encoding='utf-8')
    office_list = office_soup.find('select', attrs = {'id':'MainContent_ddlLegislators'})
   
    # empty legislator info lists to populate
    rep_names = []
    rep_tags = []
   
    # loop through legislators
    for rep in office_list.findAll('option'):
         rep_tags.append(rep['value']) # unique legislator id
         rep_names.append(rep.text) # name of legislator
    
    # remove header junk
    rep_names.pop(0)
    rep_tags.pop(0)

    # loop through legislators and scape data
    for name, rep in list(zip(rep_names, rep_tags)):
       
        print(f'\t{name}')
        URL = f"https://nmlegis.gov/Members/Legislator?SponCode={rep}"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        full_name = soup.find('span', attrs = {'id':'MainContent_formViewLegislatorName_lblLegislatorName'})
        
        # download photo
        try: 
            info = soup.find('div', attrs = {'class':'col-xs-12 col-sm-9 legislator-information'}) 
            dist = info.findAll('li', attrs = {'class':'list-group-item'})[0].a.text.replace(' ', '').zfill(2)
            pic = soup.find('img', attrs = {'id':'MainContent_formViewLegislator_imgLegislator'})['src'][2:]
            _name = name.replace(' ', '_')
            pic_path = f'https://nmlegis.gov{pic}'
            with open(f'./legislator-photos/{office_name}/{dist}_{_name}.jpg', 'wb') as f:
                f.write(requests.get(pic_path).content) 
        except: 
            next
            
