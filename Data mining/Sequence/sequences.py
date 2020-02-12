import pandas as pd

from bs4 import BeautifulSoup
import urllib
import urllib.request
import ensembl

accession_df = pd.read_csv("kinase_list.csv")
accessions = accession_df["Accession Code"]


# Opening the URL from ensembl
rna_sequences = []
dna_sequences = []
sequence_info = pd.DataFrame()

for accession in accessions:

    fail_count = 0
    failed = False
    done = False
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    request = urllib.request.urlopen(url)

    while not done:
        try:
            page = request.read(200000)
            soup = BeautifulSoup(page, 'xml')
            done = True
        except:
            fail_count += 1
            if fail_count > 10:
                failed = True
                done = True
                print("This accession did not work: ", accession)
    if failed:
        continue
    else:
        pass
    gene_id_tag = soup.find("gnCoordinate")
    protein_sequence = soup.find("sequence")
    try:
        gene_id = gene_id_tag["ensembl_gene_id"]
        trans_id = gene_id_tag["ensembl_transcript_id"]
    except:
        rna_sequences.append("NA")
        continue
    rna_sequence = ensembl.rna(trans_id)
    dna_sequence = ensembl.dna(gene_id)

    sequence_info = sequence_info.append({"Accession": accession, "DNA sequence": dna_sequence, "Transcript ID": trans_id, "RNA sequence": rna_sequence, "Protein sequence": protein_sequence}, ignore_index = True)



accession_df = pd.read_csv("substrates.csv")
accessions = accession_df["SUB_ACC_ID"]


# Opening the URL from ensembl
rna_sequences = []
dna_sequences = []
sequence_info2 = pd.DataFrame()
done_list = []
for accession in accessions:
    fail_count = 0
    done = False
    failed = False
    if accession in done_list:
        continue
    elif accession not in done_list:
        done_list.append(accession)
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession

    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            done = True
        except:
            fail_count += 1
            if fail_count > 10:
                failed = True
                print("This accession did not work: ", accession)
                done = True
    if failed:
        continue
    else:
        pass

    soup = BeautifulSoup(page, 'xml')
    gene_id_tag = soup.find("gnCoordinate")
    protein_sequence = soup.find("sequence")

    try:
        gene_id = gene_id_tag["ensembl_gene_id"]
        trans_id = gene_id_tag["ensembl_transcript_id"]
    except:
        rna_sequences.append("NA")
        continue

    rna_sequence = ensembl.rna(trans_id)
    dna_sequence = ensembl.dna(gene_id)

    if rna_sequence == "Failed on getting RNA sequence":
        continue

    if dna_sequence == "Failed at getting DNA sequence":
        continue

    sequence_info = sequence_info.append({"Accession": accession, "DNA sequence": dna_sequence, "Transcript ID": trans_id, "RNA sequence": rna_sequence, "Protein sequence": protein_sequence}, ignore_index = True)

sequence_info.to_csv("sequences_final.csv", index=False)
