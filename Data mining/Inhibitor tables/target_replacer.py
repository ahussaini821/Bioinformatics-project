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
    target = str(row["target"])
    try:
        target = target.replace("-", "")
    except:
        continue
    target = target.lower()

    for index2, row2 in names_table.iterrows():

        curr_names = str(row2["Main gene name"]) + str(row2["Other gene names"]) + str(row2["Main protein name"]) + str(row2["Other protein names"])
        curr_names = curr_names.lower()


        if target in curr_names:
            count += 1
            inhibitor_table.at[index,"target"] = row2["Accession"]
            match = True
            break

    for i in other_names:
        match2 = False

        for index2, row2 in names_table.iterrows():
            curr_names = str(row2["Main gene name"]) + str(row2["Other gene names"]) + str(row2["Main protein name"]) + str(row2["Other protein names"])
            curr_names = curr_names.lower()
            other_name = i.lower()
            if other_name == "":
                continue
            if other_name in curr_names:
                curr_acc_list.append(row2["Accession"])
                break

        curr_names = '; '.join(curr_acc_list)
        inhibitor_table.at[index,"other target"] = curr_names

    if match == True:
        print(count)
        continue


inhibitor_table.to_csv("inhibitor_kinase_acc.csv", index=False)
