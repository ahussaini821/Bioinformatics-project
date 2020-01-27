import pandas as pd

df = pd.read_csv("inhibitor_test.csv")

df.to_csv("inhibitor_kianse.csv", index=False)
