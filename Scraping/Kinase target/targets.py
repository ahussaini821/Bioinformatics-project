import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("test_list.csv")
kinase_list = df["Kinase name"]
# target_info = pd.DataFrame(columns=['Kinase', 'Target', 'Position', 'Residue'])
target_info = pd.DataFrame(columns=['Kinase', 'Phosphorylator', 'Position', 'Residue'])
target_list = []

for kinase in kinase_list:

    target_list.append(scraper.scrape(kinase, "feature(MODIFIED%20RESIDUE)"))





#target_info = pd.DataFrame(columns=['Kinase', "Kinase target"])


for index,target in enumerate(target_list):

    item_str = str(target)
    item_match = re.compile(r"MOD_RES\s([0-9]*)?;.*?\"(.*?);(.*?)\"")
    item_names = item_match.findall(item_str)


    for index2,i in enumerate(item_names):

        curr_kinase = kinase_list[index]

        if 'Phospho' not in i[1]:

            continue
        curr_residue = "NA"
        resi = i[1].replace("\"", "")
        if resi == "Phosphoserine":
            curr_residue = "Serine"
        elif resi == "Phosphotyrosine":
            curr_residue = "Tyrosine"
        elif resi == "Phosphothreonine":
            curr_residue = "Threonine"
        targets = i[2].replace('alternate','').replace(' /evidence=','').replace('autocatalysis',curr_kinase).replace(' by ','').replace('and ','').replace(',','').replace(';','')

        curr_targets_list = targets.split(' ')
        curr_pos = i[0]
        #print(type(curr_pos_list))

        for thing in curr_targets_list:
            if thing == '':
                curr_targets_list = ['NA']

        for target_index,thing in enumerate(curr_targets_list):

            target_info = target_info.append(({"Kinase": curr_kinase, "Phosphorylator": thing, "Position": curr_pos, "Residue": curr_residue}), ignore_index=True)

print(target_info)
target_info.to_csv("targets.csv", index=False)
