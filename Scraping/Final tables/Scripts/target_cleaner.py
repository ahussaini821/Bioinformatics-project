import pandas as pd

df = pd.read_csv("kinase target final2.csv")

for index, row in df.iterrows():
    #print(row["Neighbouring amino sequences"])
    if pd.isnull(row["Neighbouring amino sequences"]):
        print("poo")
        df.at[index,"Kinase accession"] = "NA"

print(df)
df.to_csv("kinase target final3.csv", index=False)
