import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("kinase_list.csv")
kinase_list = df["Kinase name"]
accession_list = df["Accession Code"]
sequence_info = pd.DataFrame(columns=['Kinase accession', 'Protein sequence'])
sequence_list = []

for accession in accession_list:

    accession = accession.lower()
    sequence_list.append(scraper.scrape(accession, "sequence"))


for index,sequence in enumerate(sequence_list):

    sequence_str = str(sequence)
    sequence_match = re.compile(r"Sequence\\n(.*)\\n")
    seq = sequence_match.findall(sequence_str)
    sequence_info = sequence_info.append({'Kinase accession': accession_list[index], 'Protein sequence': seq[0]}, ignore_index=True)

print(sequence_info)
sequence_info.to_csv("protein_sequence2.csv", index=False)



df2 = pd.read_csv("substrates.csv")

accession_list = df2["SUB_ACC_ID"]
sequence_info2 = pd.DataFrame(columns=['Kinase accession', 'Protein sequence'])
sequence_list = []
done_list = []

for accession in accession_list:
    if accession in done_list:
        continue
    done_list.append(accession)
    accession = accession.lower()
    sequence_list.append(scraper.scrape(accession, "sequence"))


for index,sequence in enumerate(sequence_list):

    sequence_str = str(sequence)
    sequence_match = re.compile(r"Sequence\\n(.*)\\n")
    seq = sequence_match.findall(sequence_str)
    try:
        sequence_info2 = sequence_info2.append({'Kinase accession': accession_list[index], 'Protein sequence': seq[0]}, ignore_index=True)
    except:
        continue

sequences_final = pd.concat([sequence_info,sequence_info2])

sequences_final.to_csv("sequences_final.csv", index=False)
