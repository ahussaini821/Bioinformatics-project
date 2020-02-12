"""
Script to generate names file containting main protein and gene name
as well as the various aliases
"""

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import urllib.request

df = pd.read_csv("substrates.csv")
accessions = df["SUB_ACC_ID"]
names_info = pd.DataFrame()
done_list = []

for accession in accessions:
    if accession not in done_list:
        done_list.append(accession)
    elif accession in done_list:
        continue
    done = False
    fail_count = 0
    alternate_names_list = []
    alternate_genes_list = []

    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    failed = 0

    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            soup = BeautifulSoup(page, 'xml')
            done = True
        except:
            fail_count += 1
            if fail_count >= 10:
                failed = 1
                print("This accession code failed: ", accession)
                done = True
            continue

    if failed == 1:
        continue
    else:
        pass

    for start in soup.find_all('fullName'):
        alternate_names_list.append(start.get_text())
    for start in soup.find_all('shortName'):
        print("poo")
        alternate_names_list.append(start.get_text())

    alternate_names = '; '.join(alternate_names_list)

    mainname_tag = soup.find("name")

    try:
        mainname = mainname_tag.get_text()
    except:
        continue

    for start in soup.find_all("gene"):

        if start["type"] == "primary":
            main_gene = start.get_text()
        else:
            alternate_genes_list.append(start.get_text())
    alternate_genes = '; '.join(alternate_genes_list)
    names_info = names_info.append({"Accession": accession, "Main protein name": mainname, "Other protein names": alternate_names, "Main gene name": main_gene, "Other gene names": alternate_genes}, ignore_index = True)
print(names_info)
names_info.to_csv("names.csv", index=False)


# This is literally the same code above just for the kinases
# Yes, there is probably a better way to do this but I am lazy
df = pd.read_csv("kinase_list.csv")
accessions = df["Accession Code"]
names_info2 = pd.DataFrame()

for accession in accessions:
    done = False
    fail_count = 0
    alternate_names_list = []
    alternate_genes_list = []

    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            soup = BeautifulSoup(page, 'xml')
            done = True
        except:
            fail_count += 1
            if fail_count >= 10:
                print("This accession code failed: ", accession)
                done = True
            continue

    for start in soup.find_all('fullName'):
        alternate_names_list.append(start.get_text())
    for start in soup.find_all('shortName'):
        print("poo")
        alternate_names_list.append(start.get_text())

    alternate_names = '; '.join(alternate_names_list)

    mainname_tag = soup.find("name")
    try:
        mainname = mainname_tag.get_text()
    except:
        continue

    for start in soup.find_all("gene"):

        if start["type"] == "primary":
            main_gene = start.get_text()
        else:
            alternate_genes_list.append(start.get_text())
    alternate_genes = '; '.join(alternate_genes_list)
    names_info2 = names_info2.append({"Accession": accession, "Main protein name": mainname, "Other protein names": alternate_names, "Main gene name": main_gene, "Other gene names": alternate_genes}, ignore_index = True)

frames = [names_info, names_info2]
result = pd.concat(frames)
result.to_csv("names_FINAL.csv", index=False)
