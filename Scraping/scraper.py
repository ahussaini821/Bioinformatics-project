import urllib
import urllib.request
import re
import pandas as pd

def scrape(kinase, info):
    curr_locations = []
    url = 'https://www.uniprot.org/uniprot/?query=' + kinase + '&columns=' + info + '&format=tab'
    request = urllib.request.urlopen(url)

    page = request.read(200000)
    return page

def appender(attribute, item_list, regex):
    df = pd.read_csv("test_list.csv")
    kinase_list = df["Kinase name"]
    item_info = pd.DataFrame(columns=['Kinase', attribute])


    for index,item in enumerate(item_list):

        item_str = str(item)
        item_match = re.compile(regex)
        item_names = item_match.findall(item_str)


        for item_name in item_names:
            item_info = item_info.append({'Kinase': kinase_list[index], attribute: item_name}, ignore_index=True)
    return item_info
