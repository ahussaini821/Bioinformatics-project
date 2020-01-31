from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Span
import pandas as pd
import math

print("start")

df = pd.read_csv("az20.tsv", sep="\t")
fold_change = list(df["AZ20_fold_change"])
sig_x = []
sig_y = []
non_x = []
non_y = []

# Iterating over rows in table and only getting values with a fold change above and below a certain threshold and putting them into their
# own list, and putting the other values into their own lists
for index, row in df.iterrows():
    if row["AZ20_fold_change"] == "inf" or row["control_mean"] == 0 or row["AZ20_fold_change"] == 1 or row["AZ20_fold_change"] == "":
        continue
    if row["AZ20_fold_change"] > 10 or row["AZ20_fold_change"] < 0.1:

        sig_x.append(row["AZ20_fold_change"])
        sig_y.append(row["AZ20_p-value"])
    else:
        non_x.append(row["AZ20_fold_change"])
        non_y.append(row["AZ20_p-value"])

# Getting the log10 of all the X-values
for index,i in enumerate(sig_x):
    curr = i

    if i == '' or i == None:
        sig_x[index] = 0

    if curr != 0:
        sig_x[index] = math.log(curr,10)

for index,i in enumerate(non_x):
    curr = i

    if i == '' or i == None:
        non_x[index] = 0

    if curr != 0:
        non_x[index] = math.log(curr,10)

TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
p_value = list(df["AZ20_p-value"])

# Getting log10 of all the y values
for index, i in enumerate(sig_y):
    sig_y[index] = (math.log(i,10))*-1

for index, i in enumerate(non_y):
    non_y[index] = (math.log(i,10))*-1


output_file("categorical.html")

# Generating the bokeh figure/plot
p = figure(tools=TOOLS)

# Plotting our points
p.circle(non_x, non_y, size=5, fill_color="orange", line_color="green", line_width=1, legend_label="Minor fold change")
p.circle(sig_x, sig_y, size=5, fill_color="blue", line_color="green", line_width=1, legend_label="Fold change > 100 or < 0.1")
p.legend.location = "top_left"
p.legend.click_policy="hide"

# A horizontal line; anything above this line has a sig P-value < 0.05
hline = Span(location=1.3, dimension='width', line_color='red', line_width=2, line_dash='dashed')
p.renderers.extend([hline])

show(p)
print(p)
