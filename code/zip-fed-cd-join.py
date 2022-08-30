#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
from pathlib import Path
import pandas as pd

## Input Data Shapefiles

# NM Congressional Districts 
input_folder = Path("../gis/nm_congressional_dist")
fp = input_folder / "nm_congressional_dist.shp"
sd = gpd.read_file(fp)
sd['DISTRICT'] = sd['OBJECTID']
sd.drop(['OBJECTID', 'District_N', 'District_1'], axis = 1, inplace=True)

# ZTCA (Zip codes)
input_folder = Path("../gis/NM_ZCTA")
fp = input_folder / "tl_2010_35_zcta510.shp"
zd_raw = gpd.read_file(fp)

# get only select columns
zd = zd_raw[['ZCTA5CE10', 'geometry']]
print(zd.crs)
zd.head()

## Join ZCTA and Districts

# join senate with zcta, senate on left
sx = gpd.sjoin(sd, zd, how = 'left', predicate = 'intersects')[["DISTRICT", "ZCTA5CE10"]]
sx.rename(columns = {'DISTRICT':'federal_district', 
                     'ZCTA5CE10':'ZCTA'}, inplace = True)

# output 
sx.to_csv('../crosswalks/fed-dist-zcta-crosswalk.csv', index = False)

for district in [1, 2, 3]: 
    out = sx[sx['federal_district'] == district]
    out.drop('federal_district', axis = 1, inplace = True)
    out.to_csv(f'../crosswalks/fed-district-{district}-zcta-crosswalk.csv', index = False)

