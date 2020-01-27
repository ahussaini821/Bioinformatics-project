import pandas as pd

inhibitor_table = pd.read_csv("new_kinase_inhibitor_list.csv")
names_table = pd.read_csv("names_final.csv")

count = 0
for index, row in inhibitor_table.iterrows():
    curr_acc_list = []
    try:
        other_names = row["other target"]
        other_names = other_names.split(" ; ")
    except:
        continue


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
    for i in other_names:
        for index2, row2 in names_table.iterrows():
            y = str(row2["Main gene name"]) + str(row2["Other gene names"]) + str(row2["Main protein name"]) + str(row2["Other protein names"])
            other_name = i.lower()
            if other_name in y:
                curr_acc_list.append(row2["Accession"])
        curr_acc = '; '.join(curr_acc_list)
        inhibitor_table.at[index,"other target"] = curr_acc
    if match == True:
        print(count)
        continue


inhibitor_table.to_csv("new_inhibitor_accession.csv", index=False)
