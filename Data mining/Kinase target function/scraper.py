"""
This script provides functions which allows the user to easily obtain specific
data using the uniprot api and appending it to a pandas dataframe
"""

import urllib
import urllib.request
import re
import pandas as pd

# This is the primary function which lets the user get information from uniprot
# requiring only the kianse accession or name and what info they want according
# to the uniprot API
def scrape(kinase, info):
    done = False
    curr_locations = []
    url = 'https://www.uniprot.org/uniprot/?query=' + kinase + '&columns=' + info + '&format=tab'
    fail_count = 0
    failed = False

    # Simply here to catch any connection errors
    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            done = True

        except:
            fail_count += 1
            if fail_count >= 10:
                done = True
                failed = True
            continue
    if failed:
        return False

    return page


# This is a function that allows the user to append relevant data to a dataframe
# and also parse the information based on a regular expression given by the
# user
def appender(attribute, item_list, regex):
    df = pd.read_csv("kinase_list.csv")
    kinase_list = df["Accession name"]
    item_info = pd.DataFrame(columns=['Kinase', attribute])


    for index,item in enumerate(item_list):

        item_str = str(item)
        item_match = re.compile(regex)
        item_names = item_match.findall(item_str)


        for item_name in item_names:
            item_info = item_info.append({'Kinase': kinase_list[index], attribute: item_name}, ignore_index=True)
    return item_info

def appender2(attribute, item_list, regex):
    df = pd.read_csv("kinase_list.csv")
    kinase_list = df["Accession Code"]
    item_info = pd.DataFrame(columns=['Kinase', attribute])
    curr_names = ''

    for index,item in enumerate(item_list):
        curr_names = ''
        item_str = str(item)
        item_match = re.compile(regex)
        item_names = item_match.findall(item_str)


        for final_index,item_name in enumerate(item_names):
            if item_name == "Protein kinase superfamily":
                continue
            if final_index != (len(item_names)-1):
                curr_names += item_name + '; '
            else:
                curr_names += item_name

        item_info = item_info.append({'Kinase': kinase_list[index], attribute: curr_names}, ignore_index=True)

    return item_info


# This is a function in case you want to separate the first item in a list
# into its own column. e.g. If you want the main gene or protein name in a
# separate column
def appender_onlyfirst(attribute, item_list, regex):
    df = pd.read_csv("kinase_list.csv")
    kinase_list = df["Accession name"]
    item_info = pd.DataFrame(columns=['Kinase', attribute])
    curr_names = ''

    for index,item in enumerate(item_list):
        curr_names = ''
        item_str = str(item)
        item_match = re.compile(regex)
        item_names = item_match.findall(item_str)




        item_info = item_info.append({'Kinase': kinase_list[index], attribute: item_names[0]}, ignore_index=True)

    return item_info
