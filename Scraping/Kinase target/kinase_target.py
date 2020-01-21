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
def phosphosite(kin_acc, kinase, target, accession, df):
    done = False

    url = 'https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&accession=' + accession
    fail_count = 0
    while not done:
        try:
            request = urllib.request.urlopen(url)
            page = request.read(200000)
            done = True
        except:
            fail_count += 1
            print("Failed connection (dna xml). Retrying...")
            if fail_count >= 10:
                done = True
                print(url)

            continue

    soup = BeautifulSoup(page, 'xml')


    gene_id_tag = soup.find("gnCoordinate")

    if gene_id_tag == None:
        bad_list.append(accession)
        print("Invalid ID?", gene_id_tag)

        return df
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
        forward = False
    elif not position:
        print(position)
    else:
        forward = True




    # This list is for later as for some reason some of the PTMs repeat
    # so this needs to be avoided
    done_list = []
    phos_pos = 0



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

        if location not in done_list:
            done_list.append(location)
        else:
            continue




        # Making sure that it is a phosphorylation PTM and we are not getting a
        # repeat entry
        if "Phospho" in phos_text and start["position"] not in done_list:
            if not forward:
                value = re.search(r":.*:.*:(.*):", position)

                phos_pos = int(value.group(1)) - int(start["position"])

                phos_pos = phos_pos * -1

            elif forward:
                value = re.search(r":.*:.*:(.*):.*:", position)
                phos_pos = int(value.group(1)) - int(start["position"])
            elif forward == "wrong":
                phos_pos = 0

            if phos_pos < 0:
                phos_pos = phos_pos * -1


        else:
            continue

        if "Phosphothreonine" in phos_text:
            resi = "T"
        elif "Phosphotyrosine" in phos_text:
            resi = "Y"
        elif "Phosphoserine" in phos_text:
            resi = "S"
        else:
            continue
        location=str(location)
        df = df.append({"Kinase accession": kin_acc, "Target accession": accession, "Location": resi+location, "Chromosome": chromosome, "Start": start["position"], "End": end["position"], "Phosphosite position": phos_pos}, ignore_index = True)

    return df

df = pd.DataFrame(columns=["Kinase accession", "Target accession", "Location", "Chromosome", "Start", "End", "Phosphosite position"])
subs = pd.read_csv("substrate_test.csv")
accessions = subs["SUB_ACC_ID"]
accessions2 = []
kinase_list = subs["KINASE"]
kinase_accession = subs["KIN_ACC_ID"]
target_list = subs["SUBSTRATE"]
target_accession = subs["SUB_ACC_ID"]
residue_list = subs["SUB_MOD_RSD"]

bad_list = []
done_list = []
for index,accession in enumerate(accessions):
    kinase = kinase_list[index]
    target = target_list[index]
    kin_acc = kinase_accession[index]

    if accession not in done_list:
        df = phosphosite(kin_acc, kinase, target, accession, df)
        done_list.append(accession)
    else:
        continue


#print(df)
df.to_csv("kinase target test2.csv", index = False)
print("FINISHED FINISHED FINISHED FINISHED FINISHED FINISHED")
