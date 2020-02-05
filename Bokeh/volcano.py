from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Span
import pandas as pd
import numpy as np
import math

def volcano(file_name):
    print("start")

    # Cleaning up the table
    df = pd.read_csv(file_name, sep="\t")
    df=df.dropna(how="all", axis=1)

    # Have to run these again after log operation
    df=df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(axis=0)

    sig = df[(df.iloc[:,3] > 10) | (df.iloc[:,3] < 0.1)]
    non_sig = df[(df.iloc[:,3] < 10) & (df.iloc[:,3] > 0.1)]
    


    sig_x = list(sig.iloc[:,3])
    sig_y = list(sig.iloc[:,4])
    non_x = list(non_sig.iloc[:,3])
    non_y = list(non_sig.iloc[:,4])

    for index,value in enumerate(sig_x):
        try:
            sig_x[index] = math.log(value,10)
        except:
            pass

    for index,value in enumerate(non_x):
        try:
            non_x[index] = math.log(value,10)
        except:
            pass
    for index,value in enumerate(non_y):
        non_y[index] = (math.log(value,10)) * -1
    for index,value in enumerate(sig_y):
        sig_y[index] = (math.log(value,10)) * -1

    sig.iloc[:,1] = sig_x
    sig.iloc[:,2] = sig_y
    sig=sig.replace([np.inf, -np.inf], np.nan)
    sig = sig.dropna(axis=0)
    sig=sig.replace(0.000000, np.nan)
    sig = sig.dropna(axis=0)

    non_sig.iloc[:,1] = non_x
    non_sig.iloc[:,2] = non_y
    non_sig=non_sig.replace([np.inf, -np.inf], np.nan)
    non_sig = non_sig.dropna(axis=0)
    non_sig=non_sig.replace(0.000000, np.nan)
    non_sig = non_sig.dropna(axis=0)


    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    output_file("categorical.html")

    # Generating the bokeh figure/plot
    p = figure(tools=TOOLS)

    # Plotting our points
    p.circle(non_sig.iloc[:,1], non_sig.iloc[:,2], size=5, fill_color="orange", line_color="green", line_width=1, legend_label="Minor fold change")
    p.circle(sig.iloc[:,1], sig.iloc[:,2], size=5, fill_color="blue", line_color="green", line_width=1, legend_label="Fold change > 100 or < 0.1")
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    p.xaxis.axis_label = 'Fold change(log10)'
    p.yaxis.axis_label = "p-value (log10)"

    # A horizontal line; anything above this line has a sig P-value < 0.05
    hline = Span(location=1.3, dimension='width', line_color='red', line_width=2, line_dash='dashed')
    p.renderers.extend([hline])

    show(p)
volcano("az20.tsv")
