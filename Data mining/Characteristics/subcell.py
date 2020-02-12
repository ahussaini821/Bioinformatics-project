"""
Script to get the information of subcellular location for each kinase using
scraper module
"""

import pandas as pd
import urllib
import urllib.request
import re

df = pd.read_csv("kinase_list.csv")
poss_subcell = pd.read_csv("subcell_locations.csv")
kinase_list = df["Accession Code"]

# A list of the possible subcellular location
# This is necessary to avoid repeats and non-relevant information
locations_list = poss_subcell["Alias"]

subcell_info = pd.DataFrame(columns=['Kinase Accession', 'Subcellular Location'])
subcell_list = []

for kinase in kinase_list:

    # Have to reinitialise the list for every kinase
    locations_list = list(poss_subcell["Alias"])

    # Made lowercase because this avoids getting results for multiple proteins
    # from uniprot
    kinase = kinase.lower()
    curr_locations = ''
    done = False
    url = 'https://www.uniprot.org/uniprot/?query=' + kinase + '&columns=comment(SUBCELLULAR%20LOCATION)&format=tab'

    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            done = True
        except:
            continue

    subcell_list.append(page)
    thing = str(page)
    curr_list = thing.split('.')

    # Checks if the item is in the possible subcell list, and if so, appends it
    for index,item in enumerate(curr_list):
        for index,location in enumerate(locations_list):
            if location in item:
                # Need to remove subcell locations already done since there
                # are repeats
                locations_list.remove(location)
                curr_locations += location + '; '
    # Gets rid of last ';' character
    curr_locations = curr_locations[:-1]
    subcell_info = subcell_info.append({'Kinase Accession': kinase, 'Subcellular Location': curr_locations}, ignore_index=True)

subcell_info.to_csv("subcell_final2.csv", index=False)
