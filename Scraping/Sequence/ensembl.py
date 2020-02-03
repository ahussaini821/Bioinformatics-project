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

      return "Failed on getting RNA sequence"

    sequence = r.text

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

      return "Failed at getting DNA sequence"

    sequence = r.text

    return sequence

def position(id):
    done = False
    server = "https://rest.ensembl.org"
    ext = "/sequence/id/" + id + "?type=genomic"
    fail_count = 0
    while not done:
        try:
            r = requests.get(server+ext, headers={ "Content-Type" : "text/x-fasta"})
            done = True
        except:
            fail_count += 1
            print("Failed connection (ensembl). Retrying...")
            if fail_count >= 10:
                print("This ID failed for position: ", id)
                done = True
            continue

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    sequence = r.text
    first_line_list = []
    for letter in sequence:
        if letter != "\n":
            first_line_list.append(letter)
        else:
            first_line = ''.join(first_line_list)
            break

    return first_line
