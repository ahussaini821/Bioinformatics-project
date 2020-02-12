import pandas as pd

from bs4 import BeautifulSoup
import urllib
import urllib.request
import ensembl

accession_df = pd.read_csv("test_list.csv")
accessions = accession_df["Accession Code"]


# Opening the URL from ensembl
rna_sequences = []
dna_sequences = []
for accession in accessions:
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    request = urllib.request.urlopen(url)

    page = request.read(200000)
    soup = BeautifulSoup(page, 'xml')
    gene_id_tag = soup.find("gnCoordinate")
    try:
        gene_id = gene_id_tag["ensembl_gene_id"]
    except:
        rna_sequences.append("NA")
        continue
    rna_sequences.append(ensembl.rna(gene_id))
    dna_sequences.append(ensembl.dna(gene_id))

# What will end up being the final dataframe with all the necessary info
sequence_info = pd.DataFrame(columns=["Gene name", "DNA Sequence", "RNA Sequence", "Protein Sequence"])

protein_df = pd.read_csv("protein_sequence.csv")
genes_df = pd.read_csv("genes_single.csv")
proteins = protein_df["Protein sequence"]
genes = genes_df["Gene names"]

for index,rna in enumerate(rna_sequences):

    sequence_info = sequence_info.append({"Gene name": genes[index], "DNA Sequence": dna_sequences[index], "RNA Sequence": rna, "Protein Sequence": proteins[index]}, ignore_index=True)
print(sequence_info)
sequence_info.to_csv("sequences.csv", index=False)
