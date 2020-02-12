"""
Script to get the information of families for each kinase using scraper module
"""

import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("kinase_list.csv")
kinase_list = df["Kinase name"]
family_info = pd.DataFrame(columns=['Kinase', 'Family'])
family_list = []

for kinase in kinase_list:
    x = scraper.scrape(kinase, "families")
    if not x:
        continue
    family_list.append(x)


family_info = scraper.appender2("Family", family_list, r"[A-Z][\sa-zA-Z\/]*family")
print(family_info)
family_info.to_csv("family_final.csv", index=False)
