import pandas as pd
from bs4 import BeautifulSoup
import urllib
import urllib.request
import ensembl

accession_df = pd.read_csv("test_list.csv")
accessions = accession_df["Accession Code"]
gene_ids = pd.DataFrame(columns=["Accession","Gene ID"])

# Opening the URL from ensembl

for accession in accessions:
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    request = urllib.request.urlopen(url)

    page = request.read(200000)
    soup = BeautifulSoup(page, 'xml')
    gene_id_tag = soup.find("gnCoordinate")
    try:
        gene_id = gene_id_tag["ensembl_gene_id"]
    except:
        continue
    gene_ids = gene_ids.append({"Accession": accession, "Gene ID": gene_id},ignore_index=True)

gene_ids.to_csv("gene_id.csv", index=False)
