import scraper
import pandas as pd
import re
#import dna_xml

names = []
df = pd.read_csv("substrates.csv")
kinase_list = df["KINASE"]
target_list = df["SUBSTRATE"]
target_accession = df["SUB_ACC_ID"]
residue_list = df["SUB_MOD_RSD"]
# target_info = pd.DataFrame(columns=['Kinase', 'Target', 'Position', 'Residue'])
target_info = pd.DataFrame(columns=['Kinase', 'Target', "Target accession", 'Target residue location'])
phos_pos = pd.read_csv("dna_xml.csv")


# for kinase in kinase_list:
#
#     target_list.append(scraper.scrape(kinase, "feature(MODIFIED%20RESIDUE)"))



#target_info = pd.DataFrame(columns=['Kinase', "Kinase target"])
for index,target in enumerate(target_list):


    target_info = target_info.append({'Kinase': kinase_list[index], 'Target': target, 'Target accession': target_accession[index], 'Target residue location': residue_list[index]}, ignore_index=True)
    for i in range(len(phos_pos.index)):
        for j in range(len(target_info.index)):
            #print(target_info.iloc[j]["Target accession"])
            #print(target_info.iloc[j]["Target residue location"][1:])
            if target_info.iloc[j]["Target accession"] == phos_pos.iloc[i]["Accession"] and target_info.iloc[j]["Target residue location"][1:] == phos_pos.iloc[i]["Location"]:
                print("poo")
                target_info.loc[j, "Chromosome"] = phos_pos.iloc[i]["Chromosome"]
                target_info.loc[j, "Start"] = phos_pos.iloc[i]["Start"]
                target_info.loc[j, "End"] = phos_pos.iloc[i]["End"]
                target_info.loc[j, "Genomic position"] = phos_pos.iloc[i]["Phosphosite position"]
            else:
                #print("no poo")
                continue
    # item_str = str(target)
    # item_match = re.compile(r"MOD_RES\s([0-9]*)?;.*?\"(.*?);(.*?)\"")
    # item_names = item_match.findall(item_str)
    #
    #
    # for index2,i in enumerate(item_names):
    #
    #     curr_kinase = kinase_list[index]
    #
    #     if 'Phospho' not in i[1]:
    #
    #         continue
    #     curr_residue = "NA"
    #     resi = i[1].replace("\"", "")
    #     if resi == "Phosphoserine":
    #         curr_residue = "Serine"
    #     elif resi == "Phosphotyrosine":
    #         curr_residue = "Tyrosine"
    #     elif resi == "Phosphothreonine":
    #         curr_residue = "Threonine"
    #     targets = i[2].replace('alternate','').replace(' /evidence=','').replace('autocatalysis',curr_kinase).replace(' by ','').replace('and ','').replace(',','').replace(';','')
    #
    #     curr_targets_list = targets.split(' ')
    #     curr_pos = i[0]
    #     #print(type(curr_pos_list))
    #
    #     for thing in curr_targets_list:
    #         if thing == '':
    #             curr_targets_list = ['NA']
    #
    #     for target_index,thing in enumerate(curr_targets_list):
    #
    #         target_info = target_info.append(({"Kinase": curr_kinase, "Phosphorylator": thing, "Residue": curr_residue, "Position": curr_pos}), ignore_index=True)

print(target_info)
#target_info.to_csv("targets.csv", index=False)
