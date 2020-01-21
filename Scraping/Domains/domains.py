import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("kinase_list.csv")
kinase_list = df["Accession Code"]
domain_info = pd.DataFrame(columns=['Kinase accession code', 'Domain', 'Domain position'])
domain_list = []

for kinase in kinase_list:

    domain_list.append(scraper.scrape(kinase, "feature(DOMAIN%20EXTENT)"))
#print(domain_list[0])

#genes_info = scraper.appender("Domain", domain_list, r"note=\"(.*?)\"")


for index,item in enumerate(domain_list):

    item_str = str(item)
    item_match = re.compile(r"note=\"(.*?)\"")
    item_match2 = re.compile(r"DOMAIN\s(.*?);")
    item_names = item_match.findall(item_str)
    item_names2 = item_match2.findall(item_str)
    print(kinase_list[index], len(item_names), len(item_names2))


    for index2,item_name in enumerate(item_names):
        domain_info = domain_info.append({"Kinase accession code": kinase_list[index], "Domain": item_name, "Domain position": item_names2[index2]}, ignore_index=True)

print(domain_info)
domain_info.to_csv("domains_final.csv", index=False)
