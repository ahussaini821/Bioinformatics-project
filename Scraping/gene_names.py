import scraper
import pandas as pd
import re

names = []
df = pd.read_csv("test_list.csv")
kinase_list = df["Kinase name"]
genes_info = pd.DataFrame(columns=['Kinase', 'Gene names'])
genes_list = []

for kinase in kinase_list:

    genes_list.append(scraper.scrape(kinase, "genes"))

#print(genes_list)

genes_info = scraper.appender("Gene names", genes_list, r"[A-Z0-9]{2,}")

# for index,gene in enumerate(genes_list):
#
#     gene_str = str(gene)
#     gene_match = re.compile(r"[A-Z0-9]{2,}")
#     gene_names = gene_match.findall(gene_str)
#
#
#     for gene_name in gene_names:
#         genes_info = genes_info.append({'Kinase': kinase_list[index], 'Gene names': gene_name}, ignore_index=True)

print(genes_info)
genes_info.to_csv("genes.csv", index=False)
