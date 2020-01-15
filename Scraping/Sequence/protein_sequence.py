import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("test_list.csv")
kinase_list = df["Kinase name"]
sequence_info = pd.DataFrame(columns=['Kinase', 'Protein sequence'])
sequence_list = []

for kinase in kinase_list:

    sequence_list.append(scraper.scrape(kinase, "sequence"))

print(sequence_list)



for index,sequence in enumerate(sequence_list):
    #print(kinase_list[index])
    sequence_str = str(sequence)
    sequence_match = re.compile(r"Sequence\\n(.*)\\n")
    seq = sequence_match.findall(sequence_str)
    # seq = seq.replace("[", "").replace("]", "")


    sequence_info = sequence_info.append({'Kinase': kinase_list[index], 'Protein sequence': seq[0]}, ignore_index=True)

print(sequence_info)
sequence_info.to_csv("protein_sequence.csv", index=False)
