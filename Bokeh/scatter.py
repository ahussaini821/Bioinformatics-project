from bokeh.plotting import figure, output_file, show
import pandas as pd
import math



print("start")
df = pd.read_csv("az20.tsv", sep="\t")
fold_change = list(df["AZ20_fold_change"])

for index,i in enumerate(fold_change):
    curr = i

    if i == '' or i == None:
        fold_change[index] = 0
        curr = 0
    if curr != 0:
        fold_change[index] = math.log(curr,10)

p_value = list(df["AZ20_p-value"])

for index, i in enumerate(p_value):
    p_value[index] = (math.log(i,10))*-1


output_file("categorical.html")

p = figure(y_range=[0,10])

p.circle(fold_change, p_value, size=5, fill_color="orange", line_color="green", line_width=1)

show(p)
