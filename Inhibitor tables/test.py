import pandas as pd

inhibitor_table = pd.read_csv("new_kinase_inhibitor_list.csv")

for index, row in inhibitor_table.iterrows():
    try:
        other_names = row["other target"]
        other_names = other_names.split(" ; ")
    except:
        continue
    for index,i in enumerate(other_names):
        other_names[index] = i.rstrip()
    print(other_names)
