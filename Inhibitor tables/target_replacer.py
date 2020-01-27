import pandas as pd

inhibitor_table = pd.read_csv("inhibitor_result.csv")
names_table = pd.read_csv("names_final.csv")

count = 0
for index, row in inhibitor_table.iterrows():
    match = False
    x = str(row["Target"])
    try:
        x = x.replace("-", "")
    except:
        continue
    for index2, row2 in names_table.iterrows():

        if x in (str(row2["Main gene name"]) + str(row2["Other gene names"]) + str(row2["Main protein name"]) + str(row2["Other protein names"])):
            count += 1

            inhibitor_table.at[index,"Target"] = row2["Accession"]
            match = True
            break
    if match == True:
        print(count)
        continue


inhibitor_table.to_csv("inhibitor_test.csv", index=False)
