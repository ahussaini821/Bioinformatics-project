from bs4 import BeautifulSoup
import urllib
import urllib.request
import pandas as pd

# Opening the URL from ensembl
url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=P31749'
request = urllib.request.urlopen(url)

page = request.read(200000)
soup = BeautifulSoup(page, 'xml')

# What will end up being the final dataframe with all the necessary info
df = pd.DataFrame(columns=["Location", "Chromosome", "Start", "End"])
gene_id_tag = soup.find("gnCoordinate")
gene_id = gene_id_tag["ensembl_gene_id"]

# Finding the chromosome number for this protein
chromosome_tag = soup.find("genomicLocation")
chromosome = chromosome_tag["chromosome"]
chromosome_start = chromosome_tag["start"]
print(chromosome_start)

# This list is for later as for some reason some of the PTMs repeat
# so this needs to be avoided
begin_list = []

# Iterating through every instance of this tag in the XML
for start in soup.find_all('ns2:begin'):
    # Getting the parent of this which is genomicLocation and then getting
    # the parent of that but only try and sometimes there is no parent for this
    # tag
    begin_parent = start.parent
    try:
        mod_type = begin_parent.parent
    except:
        continue
    # Getting all the other necessary info
    phos = mod_type.find('ns2:description')
    location_tag = mod_type.find('ns2:position')
    end = begin_parent.find("ns2:end")

    # Making sure none of the entries are empty
    if phos != None and location_tag != None:
        phos_text = phos.get_text()
        location = location_tag["position"]
    else:
        continue

    # Making sure that it is a phosphorylation PTM and we are not getting a
    # repeat entry
    if "Phospho" in phos_text and start["position"] not in begin_list:
        begin_list.append(start["position"])
        df = df.append({"Location": location, "Chromosome": chromosome, "Start": start["position"], "End": end["position"]}, ignore_index = True)
print(df)
