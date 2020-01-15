import requests, sys

def rna(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?content-type=text/plain;mask_feature=1"
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
            done = True
        except:
            continue


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


def dna(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?content-type=text/plain;mask_feature=1"
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
            done = True
        except:
            continue

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    sequence = r.text
    #print(r.text)
    return sequence
