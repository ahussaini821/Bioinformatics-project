# TO run and see the plots just type in the terminal "python3 flask_test_KSEA_analysis.py"
# "file_path" and "file_location" (in def example) need to be changed so it works on your computers
# the file used for "File_location" is the kinase_substrate_POHSPHO and is also uploaded on git
import os
from flask import Flask, render_template
import pandas as pd
import numpy as np
import scipy.stats
import statsmodels
import statsmodels.stats.multitest
import math
import bokeh
import bokeh.plotting
from bokeh.plotting import figure , output_file, show
from bokeh.embed import components




#KSEA analysis on the table provided by the user (file_to_analyze)
def KSEA_analysis(file_to_analyze, File_location):
    "The file_to_analyze is the data that the user inputs. The File_location is the Kinase-Substrate relation of PhosphositePlus"


    inhibitor_analysis = pd.read_csv(file_to_analyze, sep="\t")
    df=inhibitor_analysis[["Substrate", "control_mean","AZ20_mean","AZ20_fold_change","AZ20_p-value","AZ20_ctrlCV","AZ20_treatCV"]]

    #removing rows with at least one column empty
    df = df.dropna(axis=0)

    # calculating mean log2 of fold change of all phosphosite in the dataset and the log2(FC) standard deviation
    FC_log = np.log2(df["AZ20_fold_change"])

    #standard deviation of all phosphosites fold change(log2)
    SD_phospho= np.std(FC_log)

    FC_log_mean = FC_log.mean()

    #calculating the mean log2(FC) of known phosphosite substrates of the given kinase
    #parsing the input data to have substrate and residue location
    k_sub_loc = df.Substrate.str.split("(", n=1, expand=True)

    df["Substrates"]= k_sub_loc[0]
    #removing ")" and "_HUMAN" from the residue and substrate
    df["Location"]= k_sub_loc[1].str.replace(")",(""))
    df["Substrates"] = df["Substrates"].str.replace("_HUMAN", "")

    #removing "Substrate" column (first one)
    del df["Substrate"]


    #Getting the kinase-substrate relation from PhosphositePLUS

    K_SUB = pd.read_csv(File_location , sep="\t")

    #making all K_SUB uppercase because our dataset is also in uppercase
    K_SUB["SUBSTRATE"]= K_SUB["SUBSTRATE"].str.upper()
    K_SUB["SUB_GENE"]= K_SUB["SUB_GENE"].str.upper()

    #getting kinase and substrate that match the dataset
    #matching subtrates and residue of Phopshoite plus website with our dataset, adding the kinase
    df= df.join(K_SUB[["KINASE", "SUBSTRATE", "SUB_MOD_RSD"]].set_index(["SUBSTRATE", "SUB_MOD_RSD"]),
            on=["Substrates", "Location"])
    #matching GENE substrate and residue of Phopshoite plus website with our dataset, adding the kinase
    df= df.join(K_SUB[["KINASE", "SUB_GENE", "SUB_MOD_RSD"]].set_index(["SUB_GENE", "SUB_MOD_RSD"]),
            on=["Substrates", "Location"], rsuffix="_s")

    ##droping all rows that have not matched any kinase
    df1 = df.dropna(subset=["KINASE","KINASE_s"], how="all", axis=0)
    #saving the rows that have not a Matcehd KINASE
    df_all_SUBSTRATES_NO_KINASE = pd.concat([df,df1]).drop_duplicates(keep=False)


    ##making 1 column with kinase (using KINASE and KINASE_s) but prioritizing KINASE
    df1["KINASES"]=df1["KINASE"]
    df1["KINASES"]= np.where(df1["KINASES"].isnull(), df1["KINASE_s"], df1["KINASES"])
    df1=df1.drop(["KINASE"], axis=1)
    df1=df1.drop(["KINASE_s"], axis=1)

    df1=df1.drop_duplicates(keep="first", inplace=False)


    #counting total number of phosphosite substrates identified from the experiment that annotate to the specified kinase
    Grouping_kinases_count= df1.groupby("KINASES").size()
    #print Grouping_kinases_count
    #calculating the square root of each count
    sqrroot_all_kinases= np.sqrt(Grouping_kinases_count)
    #print sqrroot_all_kinases

    FC= np.log2(df1[["AZ20_fold_change"]])
    df1["log_FC"] = FC

    FC_Kinases = df1.groupby("KINASES")[["log_FC"]].mean()

    s_p= FC_Kinases - FC_log_mean

    s_px_sqR_m = s_p.mul(sqrroot_all_kinases, axis=0)

    z_score= s_px_sqR_m / SD_phospho
    z_score.reset_index(inplace=True)
    #print (z_score)

    #calculating significance of z_score (p-value)
    z_score["p_values"] = scipy.stats.norm.sf(abs(z_score["log_FC"]))*2

    #z_score[z_score["p_values"] < 0.05].count()
    #renaming columns
    z_score.rename(columns={"log_FC":"z_score"}, inplace=True)

    #z_score.to_csv("/Users/pedromoreno/Kinase_scores", index= False)

    z_score= z_score.sort_values(by = "z_score")
    # Just the significantly different z_scores
    z_score_sig = z_score[z_score["p_values"] < 0.05]
    output = {'z_score': z_score, "z_score_sig" : z_score_sig, "df_all_SUBSTRATES_NO_KINASE" :df_all_SUBSTRATES_NO_KINASE}

    return output

#Creating the two bar plots
def bar_plot(z_score):
    p1 = figure(x_range=z_score["KINASES"],title= " KSEA-based Protein activity", plot_width=1300)
    p1.vbar(x=z_score["KINASES"], top=z_score["z_score"], width=0.9, color = "#ff1200")
    p1.xaxis.major_label_orientation = math.pi/2
    p1.xaxis.axis_label_text_font_size = "40pt"
    p1.xaxis.axis_label = 'Kinases'
    p1.yaxis.axis_label = "Z-score"
    #output_file("z_Score_bar.html")
    return (p1)
def bar_plot1(z_score_sig):
    # creating barplot with only the significant z_scores
    p = figure(x_range=z_score_sig["KINASES"], title="Protein activity of significant activity changes",
               plot_width=1000)
    p.vbar(x=z_score_sig["KINASES"], top=z_score_sig["z_score"], width=0.5, color="#ff1200")
    p.xaxis.major_label_orientation = math.pi / 2
    p.xaxis.axis_label = 'Kinases'
    p.yaxis.axis_label = "Z-score"
    #show(p)
    return (p)



#start the web server
