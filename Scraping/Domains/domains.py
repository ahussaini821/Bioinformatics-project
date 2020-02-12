"""
Script to get the information of domains and their positions for each kinase
without the scraper module
For this we used the XML pages from EBI and BeautifulSoup
"""

from bs4 import BeautifulSoup
import urllib
import urllib.request
import pandas as pd
import re

df = pd.read_csv("kinase_list.csv")

accessions = df["Accession Code"]
domains_info = pd.DataFrame(columns=["Kinase accession code", "Domain", "Domain position"])
done_list = []
for accession in accessions:

    if accession in done_list:
        continue
    else:
        done_list.append(accession)
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    done = False
    fail_count = 0
    failed = False
    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            done = True
            soup = BeautifulSoup(page, 'xml')
        except:
            fail_count += 1
            if fail_count >= 10:
                failed = True
                done = True
    if failed:
        print("This accession failed: ", accession)
        continue

    for feature in soup.find_all("feature"):

        if feature["type"] == "domain":
            try:
                domain = feature.find("ns2:description").get_text()
                for start in feature.find_all("ns2:location"):
                    begin = start.find("ns2:begin")
                    begin_pos = begin["position"]
                    end = start.find("ns2:end")
                    end_pos = end["position"]
                    position = str(begin_pos) + ".." + str(end_pos)
                domains_info = domains_info.append({"Kinase accession code": accession, "Domain": domain, "Domain position": position}, ignore_index=True)
            except:continue


print(domains_info)
domains_info.to_csv("domains_final2.csv", index=False)
