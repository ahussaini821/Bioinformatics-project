import pandas as pd
import urllib
import urllib.request
import re
import os


df = pd.read_csv("test_list.csv")
poss_subcell = pd.read_csv("subcell_locations.csv")
kinase_list = df["Kinase name"]
locations_list = poss_subcell["Alias"]
subcell_list = []
subcell_info = pd.DataFrame(columns=['Kinase', 'Subcellular Location'])

for kinase in kinase_list:
    curr_locations = ''
    url = 'https://www.uniprot.org/uniprot/?query=' + kinase + '&columns=comment(SUBCELLULAR%20LOCATION)&format=tab'
    request = urllib.request.urlopen(url)

    page = request.read(200000)
    subcell_list.append(page)

    thing = str(page)
    curr_list = thing.split('.')
    for index,item in enumerate(curr_list):

        for location in locations_list:
            if location in item:

                curr_locations += location + '; '

    curr_locations = curr_locations[:-1]
    subcell_info = subcell_info.append({'Kinase': kinase, 'Subcellular Location': curr_locations}, ignore_index=True)

    # file_name = str(kinase) + '.txt'
    # urllib.request.urlretrieve(url, file_name)
    # kinase_info = open(file_name, "r")



#single_kinase.write(str(test_list[0]))
# for kinase in subcell_list:
#     curr_locations = []
#     thing = str(kinase)
#     curr_list = thing.split('.')
#
#     for item in curr_list:
#
#         for location in locations_list:
#             if location in item:
#                 curr_locations.append(location)
#
#     for i in curr_locations:
#         subcell_info = subcell_info.append({'Kinase': kinase, 'Subcellular Location': i}, ignore_index=True)

subcell_info.to_csv("subcell2.csv", index=False)
