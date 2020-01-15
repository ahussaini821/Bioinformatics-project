import requests, sys

def rna(id):

    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?content-type=text/plain;mask_feature=1"

    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    sequence = r.text
    #print(r.text)
    rna_list = []
    for base in sequence:
        if base.isupper():
            rna_list.append(base)
    for index,base in enumerate(rna_list):
        if base == "T":
            rna_list[index] = "U"
    return ''.join(rna_list)
