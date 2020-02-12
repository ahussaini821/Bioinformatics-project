"""
Script to get the uniprot links for each kinase
"""

import pandas as pd
import re

df = pd.read_csv("substrates.csv")
accessions = df["SUB_ACC_ID"]
function_info = pd.DataFrame(columns=["Accession code", "Uniprot URL"])
done = []
for accession in accessions:
    if len(accession) > 10:
        continue
    if accession not in done:

        url = 'https://www.uniprot.org/uniprot/' + accession
        function_info = function_info.append({"Accession code": accession, "Uniprot URL": url}, ignore_index = True)
        done.append(accession)
    elif accession in done:
        continue


print(function_info)
function_info.to_csv("substrate_functions.csv", index=False)
