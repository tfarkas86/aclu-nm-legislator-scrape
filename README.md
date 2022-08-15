# aclu-nm-legislator-scrape

This repo contains scripts to automatically harvest information about current New Mexico legislators and output CSVs with all information.  

Data about individual legislators is scraped from https://nmlegis.gov/. Photographs of each legislator are automatically downloaded.  

Links to congressional district maps are scrapted from https://www.sos.state.nm.us/voting-and-elections/data-and-maps/. 

The list of ZCTAs (zip code tabulation areas) are derived from a spatial join of congressional districts and ZCTA boundaries, taken from http://rgis.unm.edu/rgis6/. 

Some post-processing of the output files is required. The two CSVs should be "imported" into a single Excel with UTF-8 encoding to properly render accented characters, and the map links need to be manually linked with `=HYPERLINK()'. 
