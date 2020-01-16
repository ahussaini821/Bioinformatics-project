from bs4 import BeautifulSoup
import urllib
import urllib.request
import pandas as pd
import ensembl
import re

location_list = []
chromosome_list = []
start_list = []
end_list = []
bases_list = []
# Opening the URL from ensembl
def phosphosite(accession):
    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    request = urllib.request.urlopen(url)

    page = request.read(200000)
    soup = BeautifulSoup(page, 'xml')

    # What will end up being the final dataframe with all the necessary info
    df = pd.DataFrame(columns=["Location", "Chromosome", "Start", "End", "Bases around Phosphosite"])
    gene_id_tag = soup.find("gnCoordinate")
    gene_id = gene_id_tag["ensembl_gene_id"]

    # Finding the chromosome number for this protein
    chromosome_tag = soup.find("genomicLocation")
    chromosome = chromosome_tag["chromosome"]
    chromosome_start = chromosome_tag["start"]
    #print(chromosome_start)

    gene_id_tag = soup.find("gnCoordinate")
    gene_id = gene_id_tag["ensembl_gene_id"]

    position = ensembl.position(gene_id)
    if position[-2] == "-":
        print("poo")
        forward = False
    else:
        forward = True
        print("poo2")

    sequences_df = pd.read_csv("sequences.csv")
    dna_sequence = sequences_df.at[0,"DNA Sequence"]
    dna_sequence = dna_sequence.upper()

    # This list is for later as for some reason some of the PTMs repeat
    # so this needs to be avoided
    begin_list = []
    phos_pos = []



    # Iterating through every instance of this tag in the XML
    for start in soup.find_all('ns2:begin'):
        # Getting the parent of this which is genomicLocation and then getting
        # the parent of that but only try and sometimes there is no parent for this
        # tag
        phos_pos = 0
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
            if not forward:
                value = re.search(r":.*:.*:(.*):", position)
                phos_pos = int(value.group(1)) - int(start["position"])

            elif forward:
                value = re.search(r":.*:.*:(.*):.*:", position)
                phos_pos = int(value.group(1)) - int(start["position"])
            lower_site = dna_sequence[phos_pos:phos_pos+3].lower()
            final = dna_sequence[phos_pos-15:phos_pos] + lower_site + dna_sequence[phos_pos+3:phos_pos+18]

            codon = dna_sequence[phos_pos:phos_pos+3]
            #print(codon,final)
            begin_list.append(start["position"])
            df = df.append({"Location": location, "Chromosome": chromosome, "Start": start["position"], "End": end["position"], "Bases around Phosphosite": final}, ignore_index = True)
    print(df)


phosphosite("P31749")
