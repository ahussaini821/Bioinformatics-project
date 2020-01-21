import urllib
import urllib.request
import re
import pandas as pd
import requests

df = pd.read_csv("substrate_test.csv")
df2 = pd.read_csv("genes.csv")
target_list = df["SUB_ACC_ID"]
gene_list = df["SUB_GENE"]
genes_info = pd.DataFrame(columns=['Accession code', 'Gene name', 'Aliases'])


for index,target in enumerate(target_list):
    done = False

    url = 'https://www.uniprot.org/uniprot/?query=' + target + '&columns=genes&format=tab'
    while not done:
        try:
            response = requests.get(url)
            page = response.text
            done = True


        except:
            fail_count += 1
            if fail_count >= 10:
                print("Connection failed with 10 attempts")
                print("Failed accession: ", target)
                done = True
            continue
    mo = re.findall(gene_list[index]+r".*", page)

    aliases = mo[0].split(' ')
    for alias in aliases:
        if index == 0:
            genes_info = genes_info.append({"Accession code": target, "Gene name": alias}, ignore_index=True)
        genes_info = genes_info.append({"Accession code": target, "Gene names": alias}, ignore_index=True)

#print(genes_info)

frames = [df2, genes_info]

result = pd.concat(frames)
print(result)
result.to_csv("names_test.")
