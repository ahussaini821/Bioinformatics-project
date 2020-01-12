import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("test_list.csv")
kinase_list = df["Kinase name"]
family_info = pd.DataFrame(columns=['Kinase', 'Family'])
family_list = []

for kinase in kinase_list:

    family_list.append(scraper.scrape(kinase, "families"))

#print(family_list[0])

family_info = scraper.appender("Family", family_list, r"[A-Z][\sa-zA-Z\/]*family")
print(family_info)
family_info.to_csv("family.csv", index=False)
