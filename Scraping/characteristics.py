import pandas as pd
kinase_list = pd.read_csv("test_list.csv")
kinase_names = kinase_list["Kinase name"]

genes_list = pd.read_csv("genes_single.csv")
gene_names = genes_list["Gene names"]

subcell_list = pd.read_csv("subcell2.csv")
subcell_names = subcell_list["Subcellular Location"]

characteristics = pd.DataFrame(columns=["Kinase ID", "Gene ID", "Subcellular location"])

for index,kinase in enumerate(kinase_names):


    characteristics = characteristics.append({"Kinase ID": kinase, "Gene ID": gene_names[index], "Subcellular location": subcell_names[index]}, ignore_index=True)

print(characteristics)
characteristics.to_csv("characteristics.csv", index=False)
