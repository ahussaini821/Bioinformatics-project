import pandas as pd

df = pd.read_csv("kinase target final.csv")

df.fillna(0, inplace=True)

print(df)
df.to_csv("kinase target final no na.csv", index=False)
