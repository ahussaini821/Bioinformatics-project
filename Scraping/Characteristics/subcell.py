import pandas as pd
import urllib
import urllib.request
import re

df = pd.read_csv("kinase_list.csv")
poss_subcell = pd.read_csv("subcell_locations.csv")
kinase_list = df["Accession Code"]
locations_list = poss_subcell["Alias"]
subcell_info = pd.DataFrame(columns=['Kinase Accession', 'Subcellular Location'])
subcell_list = []

for kinase in kinase_list:

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

    for index,item in enumerate(curr_list):
        for location in locations_list:
            if location in item:
                curr_locations += location + '; '

    curr_locations = curr_locations[:-1]
    subcell_info = subcell_info.append({'Kinase Accession': kinase, 'Subcellular Location': curr_locations}, ignore_index=True)

subcell_info.to_csv("subcell_final.csv", index=False)
