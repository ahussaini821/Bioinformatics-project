from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Span
import pandas as pd
import math
import numpy as np

print("start")




df = pd.read_csv("az20.tsv", sep="\t")

#keeping necessary columns
df=df.dropna(how="all", axis=1)

df=df.replace([np.inf, -np.inf], np.nan)
#removing rows with at least one column empty
df = df.dropna(axis=0)


fold_change = list(df["AZ20_fold_change"])
sig_x = []
sig_y = []
non_x = []
non_y = []

# Iterating over rows in table and only getting values with a fold change above and below a certain threshold and putting them into their
# own list, and putting the other values into their own lists
for index, row in df.iterrows():
    # Attempting to get rid of bad values from table; doesn't work as intended. Can probably be removed safely
    if row["AZ20_fold_change"] == "inf" or row["control_mean"] == 0 or row["AZ20_fold_change"] == 1 or row["AZ20_fold_change"] == "":
        continue

    # Threshold check
    if row["AZ20_fold_change"] > 10 or row["AZ20_fold_change"] < 0.1:

        sig_x.append(row["AZ20_fold_change"])
        sig_y.append(row["AZ20_p-value"])
    else:
        non_x.append(row["AZ20_fold_change"])
        non_y.append(row["AZ20_p-value"])

# Getting the log10 of all the X-values
for index,i in enumerate(sig_x):
    curr = i

    # Can't get log of None values so these need to be taken care of
    # Can probably be safely removed at this point thanks to earlier check
    if i == '' or i == None:
        sig_x[index] = 0

    if curr != 0:
        sig_x[index] = math.log(curr,10)

# Same as above
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
sig_x2 = []
sig_y2 = []
for index, value in enumerate(sig_x):
    test = str(value)
    if test != '0.0':

        sig_x2.append(float(value))
        sig_y2.append(float(value))

output_file("categorical.html")

# Generating the bokeh figure/plot
p = figure(tools=TOOLS)

# Plotting our points
p.circle(non_x, non_y, size=5, fill_color="orange", line_color="green", line_width=1, legend_label="Minor fold change")
p.circle(sig_x, sig_y, size=5, fill_color="blue", line_color="green", line_width=1, legend_label="Fold change > 100 or < 0.1")
p.legend.location = "top_left"
p.legend.click_policy="hide"
p.xaxis.axis_label = 'Fold change(log10)'
p.yaxis.axis_label = "p-value (log10)"

# A horizontal line; anything above this line has a sig P-value < 0.05
hline = Span(location=1.3, dimension='width', line_color='red', line_width=2, line_dash='dashed')
p.renderers.extend([hline])

show(p)
