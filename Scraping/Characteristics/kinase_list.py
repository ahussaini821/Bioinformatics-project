"""
Script to generate the list of human kinases from the text file from uniprot
"""

import re
import pandas as pd


kinases = open("kinase.txt", "r")
kinase_names = []
accessions = []
subcell_list = []
for line in kinases:
    mo = re.findall(r"[a-zA-Z0-9]*\s*([a-zA-Z0-9]*_[a-zA-Z0-9]*)\s*\((.*)\s{4}\)",line)

    if len(mo) > 0:
        kinase_names.append(mo[0][0])
        accessions.append(mo[0][1])


d = {"Kinase name": kinase_names, "Accession Code": accessions}
df = pd.DataFrame(data=d)
print(df)
df.to_csv("kinase_list.csv", index=False)
