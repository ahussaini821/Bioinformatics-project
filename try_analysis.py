#tis is the code about sunburst chart
#because it just run my jupyter book so if you should try it on falsk you should import flask
#install plotly in python first
from flask import Flask,render_template
import pandas as pd
import numpy as np
import math
import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

#1
#first deal with data
#remove empty
#file_to_analyze means the file user upload
#in this example we use az20.csv
#file_to_analyze='az20.csv'
def remove_empty(file_to_analyze):
    df= pd.read_csv(file_to_analyze)
    namelist=df.columns.values.tolist()
    list_name=[]
    for i in namelist:
        if 'fUnnamed'not in i:
            if '\n'not in i:
                list_name.append(i)
    df1=df[list_name]#extract the column
    df1.replace(to_replace=r'^\s*$',value=np.nan,regex=True,inplace=True)
    Df= df1.dropna()#remove empty
    print("ok")
    Df.to_csv('no empty '+file_to_analyze)
#after run this function,we can get the file "no empty az20.csv"
#no empty az20.csv" has already remove all empty

#2
#separate them by pvalue
#because user maybe want just see p-value<0.05
#so use this function to separate which one p-value<0.05
def p_value_005(file_to_analyze):
        data1= pd.read_csv('no empty '+file_to_analyze)
        rows = data1.shape[0]
        p_value_005 = pd.DataFrame()
        for i in range (0, rows):
            if data1['AZ20_p-value'][i] >0.05:
                pass
            else:
                p_value_005 = pd.concat([p_value_005, data1.iloc[[i],:]], axis = 0, ignore_index = True)
        return p_value_005 #return the dataframe which pvalue<0.05
#after finished it we can use this function to get the dataframe which pvalue<0.05

#3
#separate them by fold change
#because user maybe want just see positive or negative fold change
#so use this function to separate it

#this one (p-value<0.05)
#positive
def fold_change_positive_005(file_to_analyze):
    df1=p_value_005(file_to_analyze)
    rows = df1.shape[0]
    fold_change_005_positive= pd.DataFrame()
    fold_change_005_no_function= pd.DataFrame()
    fold_change_005_negative= pd.DataFrame()
    for i in range (0, rows):
        if df1['AZ20_fold_change'][i] >1:
            fold_change_005_positive= pd.concat([fold_change_005_positive, df1.iloc[[i],:]], axis = 0, ignore_index = True)
    return(fold_change_005_positive)
#this one (p-value<0.05)

def sunburst_005(file_to_analyze):
    #first collect data what we need
    data1=pd.read_csv(file_to_analyze)#read the file user upload
    
    remove_empty(file_to_analyze)#use the function "remove empty"at first(you can see it at #1)
    data2=pd.read_csv('no empty '+file_to_analyze)#read the file"no empty"
    
    p_value_005(file_to_analyze)#use the function "separate p_value by 0.05"(you can see it at #2)
    data3=p_value_005(file_to_analyze)#read the dataframe which p-value<0.05
    
    fold_change_positive_005(file_to_analyze)#use the function "extract the fold change which is positive"(you can see it at #3)
    data4=fold_change_positive_005(file_to_analyze)#read the dataframe which fold change is positive
    
    #second creat list for chart
    all_category=['empty','have value','p>0.05','p<=0.05','positive','negative']
    link_with_category_one_to_one=['','','have value','have value','p<=0.05','p<=0.05']
    a1=len(data2)/len(data1)
    a2=1-a1
    b1=len(data3)/len(data2)
    b1=b1*a1
    b2=a1-b1
    c1=len(data4)/len(data3)
    c1=c1*b1
    c2=b1-c1
    value1=[a2,a1,b2,b1,c1,c2]
    
    #third now we generate the sunbrust chart
    fig =go.Figure(go.Sunburst(
        labels=all_category,
        parents=link_with_category_one_to_one,
        values=value1,
        branchvalues="total",
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.write_html('templates/sunburst.html')

#####example="az20.csv"
file_to_analyze="az20.csv"
sunburst_005(file_to_analyze)

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('sunburst.html')




