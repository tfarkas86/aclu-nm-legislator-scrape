#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
from pathlib import Path
import pandas as pd

## Input Data Shapefiles

# Senate
input_folder = Path("../gis/NM_Senate")
fp = input_folder / "NM_Senate.shp"
sd = gpd.read_file(fp)

# House
input_folder = Path("../gis/NM_House")
fp = input_folder / "NM_House.shp"
hd = gpd.read_file(fp)

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
sx.rename(columns = {'DISTRICT':'senate_district', 
                     'ZCTA5CE10':'ZCTA'}, inplace = True)

# join house with zcta
hx = gpd.sjoin(hd, zd, how = 'left', predicate = 'intersects')[["DISTRICT", "ZCTA5CE10"]]
hx.rename(columns = {'DISTRICT':'house_district', 
                     'ZCTA5CE10':'ZCTA'}, inplace = True)

# join zcta with house and senate
zx1 = gpd.sjoin(zd, hd, how = 'left', predicate = 'intersects')[['ZCTA5CE10','DISTRICT', 'geometry']]
zx1.rename(columns = {'ZCTA5CE10':'ZCTA', 
                      'DISTRICT':'house_district'}, inplace = True)
zx2 = gpd.sjoin(zx1, sd, how = 'left', predicate = 'intersects')[['ZCTA', 'house_district', 'DISTRICT']]
zx2.rename(columns = {'DISTRICT':'senate_district'}, inplace = True)

# output 
sx.to_csv('../crosswalks/senate-zcta-crosswalk.csv', index = False)
hx.to_csv('../crosswalks/house-zcta-crosswalk.csv', index = False)

# string concat
(
sx.
    sort_values(['ZCTA']).
    groupby(['senate_district']).agg(', '.join).reset_index().
    to_csv('../crosswalks/senate-zcta-crosswalk-comma-sep.csv', index = False)
)
(
hx.
    sort_values(['ZCTA']).
    groupby(['house_district']).agg(', '.join).reset_index().
    to_csv('../crosswalks/house-zcta-crosswalk-comma-sep.csv', index = False)
)
