import pandas as pd

df = pd.read_csv("01conc.csv")

x = df["Target"]
for target in x:
    print(target)
