import requests 
from bs4 import BeautifulSoup
import pandas as pd

# loop over offices, then navigate to pages for each legislator and scrape data
for office_identifier, office_name in zip(['R', 'S'], ['House', 'Senate']):
    
    print(office_name)
    office_url = f'https://nmlegis.gov/Members/Legislator_List?T={office_identifier}'
    r_office = requests.get(office_url)
    office_soup = BeautifulSoup(r_office.content, 'html5lib')
    #office = office_soup.find('a', attrs = {'id':'siteMapBreadcrumbs_lnkPage_2'}) # get office from page
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

    dictlist = [] # empty list for dicsts to combine into data frame

    # loop through legislators and scape data
    for name, rep in zip(rep_names, rep_tags):
        print(f'\t{name}')
        URL = f"https://nmlegis.gov/Members/Legislator?SponCode={rep}"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        full_name = soup.find('span', attrs = {'id':'MainContent_formViewLegislatorName_lblLegislatorName'})
        party = full_name.text[(full_name.text.find('(') + 1):full_name.text.find(')')]
        info = soup.find('div', attrs = {'class':'col-xs-12 col-sm-9 legislator-information'}) 
        
        out_dict = {'Legislator':name, 'Party':party, 'Office':office_name} # initialize dict to hold infoi

        # loop through info elements and add to dict
        for row in info.findAll('li', attrs = {'class':'list-group-item'}):
            attr = row.b.text
            attr = attr.replace(':', '')
            # handle cases where info is in span vs a elements, also if empty
            try: 
                datum = row.a.text
            except: 
                try: 
                    info_row = str(row.span).replace('<br/>', ', ')
                    info_soup = BeautifulSoup(info_row, 'html5lib')
                    datum = info_soup.text
                except: 
                    datum = ''
            dict_add = {attr:datum}
            out_dict.update(dict_add)
        
        dictlist.append(out_dict) # concatenate with growing dict 

    df = pd.DataFrame(dictlist) # create DataFrame from list of dicts
    
    # write DataFrame out to one CSV for each office. 
    df.to_csv(f'NM_{office_name}_legislator_info.csv', index = False)
