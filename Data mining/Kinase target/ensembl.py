"""
A group of functions to get information from ensembl such as DNA, RNA and protein
sequences
"""

import requests, sys



def rna(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?type=cdna"
    fail_count = 0
    failed = False
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
            done = True
        except:
            fail_count += 1
            if fail_count >= 10:
                done = True
                print("This transcript ID didn't work: ", id)
                failed = True

            continue
    if failed:
        return "Failed on getting RNA sequence"



    if not r.ok:
      # r.raise_for_status()
      # sys.exit()
      return "Failed on getting RNA sequence"

    sequence = r.text
    #print(r.text)
    return sequence



def dna(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?type=genomic"
    fail_count = 0
    failed = False
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
            done = True
        except:
            fail_count += 1
            if fail_count >= 10:
                done = True
                failed = True
                done = True
            continue
    if failed:
        return "Failed at getting DNA sequence"

    if not r.ok:
      # r.raise_for_status()
      # sys.exit()
      return "Failed at getting DNA sequence"

    sequence = r.text
    #print(r.text)
    return sequence

def position(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?type=genomic"
    fail_count = 0
    failed = False
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
            done = True
        except:
            fail_count += 1
            print("Failed connection (ensembl). Retrying...")
            if fail_count >= 10:
                print("This ID failed for position: ", id)
                failed = True
                done = True
            continue
    if failed:
        return False
    if not r.ok:
      return False

    sequence = r.text
    first_line_list = []
    for letter in sequence:
        if letter != "\n":
            first_line_list.append(letter)
        else:
            first_line = ''.join(first_line_list)
            break



    #print(r.text)
    return first_line
