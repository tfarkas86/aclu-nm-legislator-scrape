#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd

# loop house and senate to get links and join to existing legislator files
for on_lower in ['house', 'senate']: 
    URL = f'https://www.sos.state.nm.us/voting-and-elections/data-and-maps/{on_lower}-district-maps/'
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    # get map links
    tables = soup.find('table')
    dict_list = []
    for i in tables.tbody.findAll('tr'):
        dis_text = i.find_next('td').text
        lnk_text = i.find_all('td')[1].find_next('a')['href']
        if (re.search('[0-9]+', dis_text) is not None): 
            dict_list.append({f'{on_lower}_district':re.findall('[0-9]+', dis_text)[0], 
                           'Map Link':lnk_text})
    df_link = pd.DataFrame(dict_list)

    # join with legislator file
    ld = pd.read_csv(f'./legislator-info/nm_{on_lower}_legislator_info.csv').drop(['Map Link'], axis = 1)
    df_link[f'{on_lower}_district'] = df_link[f'{on_lower}_district'].astype('int64')
    merged_df = ld.merge(df_link, how = 'left', left_on = 'District', right_on = f'{on_lower}_district').drop([f'{on_lower}_district'], axis = 1)

    # output to Excel
    merged_df.to_excel(f'legislator-info/nm-{on_lower}-legislator-info.xlsx')

