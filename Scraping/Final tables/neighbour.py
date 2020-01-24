import pandas as pd

df = pd.read_csv("substrates.csv")
df2 = pd.read_csv("kinase target final.csv")
count = 0
for index, row in df.iterrows():

    match = False

    for index2, row2 in df2.iterrows():
        if match == True:
            break
        if row["SUB_ACC_ID"] == row2["Target accession"] and row["SUB_MOD_RSD"] == row2["Location"] and row["KIN_ACC_ID"] == row2["Kinase accession"]:
            count += 1
            print("match", count)
            df2.loc[index2, 'Neighbouring amino sequences'] = row["SITE_+/-7_AA"]
            match = True
            continue
    if match == True:
        continue

df2.to_csv("kinase target final2.csv", index=False)
