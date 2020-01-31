from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, GroupFilter, Span
import pandas as pd
import math

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
p = figure(x_range=fruits, plot_height=250, title="Fruit Counts",
           toolbar_location=None, tools="")

p.vbar(x=fruits, top=[-2, 3, -6, 2, 4, 6], width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
