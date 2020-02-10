import csv
from flask import Flask,render_template
import pandas as pd
import numpy as np
import math
import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from pandas import Series

app = Flask(__name__)

def remove_empty(file_to_analyze):
    df= pd.read_csv(file_to_analyze, sep='\t')
    namelist=df.columns.values.tolist()
    list_name=[]
    #print(len(df))
    for i in namelist:
        if 'Unnamed'not in i:
            if '\n'not in i:
                list_name.append(i)
    df1=df[list_name]#extract the column
    temporary= pd.DataFrame()
    temporary_name=[]
    list_name2=list_name
    list_name2.remove("Substrate")
    list_name2.remove("control_mean")
    list_name3=[]
    if len(list_name)>10:
        for name in list_name2:
            if '_treatCV'in name:
                nPos=name.find('_')
                new_name=name[0:nPos]
                list_name3.append(name)
                list_name3.append("control_mean")
                list_name3.append("Substrate")
                df0= pd.DataFrame()
                df0=df[list_name3]
                newname0=[]
                for number in range(0,len(df0)):
                    newname0.append(new_name)
                    #df0['inhibitor']=newname0
                df0.insert(len(df0.columns), 'inhibitor', newname0)
                df0.columns =['mean', 'fold_change', 'P-value', 'ctrlCV', 'treatCV',"control_mean","Substrate",'inhibitor']
                list_name3=[]
                temporary = pd.concat([temporary,df0])
            else:
                list_name3.append(name)
    else:
        temporary=df1
    temporary.to_csv("have_empty.csv")
    temporary.replace(to_replace=r'^\s*$',value=np.nan,regex=True,inplace=True)
    Df=temporary.dropna()#remove empty
    print("ok")
    Df.to_csv('no_empty.csv')
    Df.to_csv('no_empty.tsv')
    return "ok"

def p_value_005(file_to_analyze):
    data1= pd.read_csv('no_empty.csv')
    rows = data1.shape[0]
    p_value_005 = pd.DataFrame()
    namelist=data1.columns.values.tolist()
    list_name=[]
    #print(len(df))
    for i in namelist:
        if 'Unnamed'not in i:
            if '\n'not in i:
                list_name.append(i)
    name=''
    for i in list_name:
        if 'value' in i:
            name=i
    for i in range (0, rows):
        if data1[name][i] >0.05:
            pass
        else:
            p_value_005 = pd.concat([p_value_005, data1.iloc[[i],:]], axis = 0, ignore_index = True)
    p_value_005.to_csv("p_value005.csv")
    return "ok"



def fold_change_positive_005(file_to_analyze):
    df1=pd.read_csv("p_value005.csv")
    rows = df1.shape[0]
    fold_change_005_positive= pd.DataFrame()
    fold_change_005_negative= pd.DataFrame()
    data1= pd.read_csv('no_empty.csv')
    namelist=data1.columns.values.tolist()
    list_name=[]
    #print(len(df))
    for i in namelist:
        if 'Unnamed'not in i:
            if '\n'not in i:
                list_name.append(i)
    name=''
    for i in list_name:
        if 'fold_change' in i:
            name=i
    for i in range(0,rows):
        if df1[name][i] >1:
            fold_change_005_positive= pd.concat([fold_change_005_positive, df1.iloc[[i],:]], axis = 0, ignore_index = True)
        else:
            fold_change_005_negative= pd.concat([fold_change_005_negative, df1.iloc[[i],:]], axis = 0, ignore_index = True)
    fold_change_005_positive.to_csv("positive005.csv")
    fold_change_005_negative.to_csv("negative.csv")
    return"ok"

def sunburst_base(file_to_analyze):

    data1=pd.read_csv("have_empty.csv")#read the file user upload

    data2=pd.read_csv('no_empty.csv')#read the file"no empty"

    data3=pd.read_csv("p_value005.csv")#read the dataframe which p-value<0.05

    data4=pd.read_csv("positive005.csv")#read the dataframe which fold change is positive
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
    with open('.vscode/templates/plotly_graph_sunburst.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))  #third now we generate the sunbrust chart

    return "ok"



@app.route('/',)
def synchronize():
    file_to_analyze="mux.tsv"
    a=remove_empty(file_to_analyze)
    b=p_value_005(file_to_analyze)
    c=fold_change_positive_005(file_to_analyze)
    d=sunburst_base(file_to_analyze)
    return render_template('plotly_graph_sunburst.html')


if __name__=="__main__":#如果以app.py当成主程序执行
    app.run()#立刻启动伺服务器