import pandas as pd

kinase_list = pd.read_csv("kinase_list.csv")
kinase_names = kinase_list["Accession Code"]


subcell_list = pd.read_csv("subcell_final2.csv")
subcell_names = subcell_list["Subcellular Location"]

family_list = pd.read_csv("family_final.csv")
family_names = family_list["Family"]

characteristics = pd.DataFrame(columns=["Kinase Accession", "Family", "Subcellular location"])

for index,kinase in enumerate(kinase_names):

    characteristics = characteristics.append({"Kinase Accession": kinase, "Family": family_names[index], "Subcellular location": subcell_names[index]}, ignore_index=True)


characteristics.to_csv("characteristics_final.csv", index=False)
