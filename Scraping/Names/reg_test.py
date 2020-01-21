import re

ting = "Gene names\nEif2ak3 Pek Perk\nEIF2S3 EIF2G\nEIF2S2 EIF2B\nDDX3X DBX DDX3\nEIF2S1 EIF2A\nEIF2AK2 PKR PRKR\nACTN1"
print(ting)
gene = "EIF2S1"

mo = re.findall(gene+r".*", ting)
print(mo)
