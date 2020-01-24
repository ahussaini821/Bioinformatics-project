import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("test_list.csv")
kinase_list = df["Kinase name"]
name_info = pd.DataFrame(columns=['Kinase', 'Other names'])
name_list = []

for kinase in kinase_list:

    name_list.append(scraper.scrape(kinase, "protein%20names"))



name_info = scraper.appender("Other names", name_list, r"\\n(.*?)\s\(.*?\).*?")
name_info2 = scraper.appender("Other names", name_list, r"\(([^EC].*?)\)")
frames = [name_info, name_info2]
final = pd.concat(frames)

for index,name in enumerate(name_list):
    name_str = str(name)
    first_name_match = re.compile(r"\\n(.*?)\s\(.*?\).*?")
    first_name = first_name_match.findall(name_str)
    name_info = name_info.append({'Kinase': kinase, 'Other names': first_name[0]}, ignore_index=True)

    other_names_match = re.compile(r"\(([^EC].*?)\)")
    other_names = other_names_match.findall(name_str)

    for i in other_names:
        
        name_info = name_info.append({'Kinase': kinase_list[index], 'Other names': i}, ignore_index=True)

print(name_info)
name_info.to_csv("names.csv", index=False)
