import pandas as pd

df = pd.read_csv("kinase target final.csv")


for index, row in df.iterrows():
    if int(row["Start"]) > int(row["End"]):
        curr_end = row["End"]
        curr_start = row["Start"]
        df.at[index,"Start"] = curr_end
        df.at[index,"End"] = curr_start

df.to_csv("kinase target final2.csv", index=False)
