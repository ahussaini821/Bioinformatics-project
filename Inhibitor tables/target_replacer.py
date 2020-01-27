import pandas as pd

inhibitor_table = pd.read_csv("new_kinase_inhibitor_list.csv")
names_table = pd.read_csv("names_final.csv")

count = 0
for index, row in inhibitor_table.iterrows():
    match = False
    x = str(row["target"])
    try:
        x = x.replace("-", "")
    except:
        continue
    x = x.lower()
    for index2, row2 in names_table.iterrows():
        y = str(row2["Main gene name"]) + str(row2["Other gene names"]) + str(row2["Main protein name"]) + str(row2["Other protein names"])
        y = y.lower()

        if x in y:
            count += 1

            inhibitor_table.at[index,"target"] = row2["Accession"]
            match = True
            break
    if match == True:
        print(count)
        continue


inhibitor_table.to_csv("inhibitor_test.csv", index=False)
