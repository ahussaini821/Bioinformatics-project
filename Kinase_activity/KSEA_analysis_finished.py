
# TO run and see the plots just type in the terminal "python3 KSEA_analysis_finished.py"
# "file_path" and "file_location" (in def example) need to be changed so it works on your computers
# the file used for "File_location" is the kinase_substrate_POHSPHO and is also uploaded on git
from flask import Flask, render_template
import pandas as pd
import numpy as np
import scipy.stats
import math
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import  Span

#create flask application
app = Flask(__name__)


#creating volcanoplot
def volcano(file_name):


    # Cleaning up the table
    df = pd.read_csv(file_name, sep="\t")
    df = df.dropna(how="all", axis=1)

    # Have to run these again after log operation
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(axis=0)

    sig = df[(df.iloc[:, 3] > 10) | (df.iloc[:, 3] < 0.1)]
    non_sig = df[(df.iloc[:, 3] < 10) & (df.iloc[:, 3] > 0.1)]

    sig_x = list(sig.iloc[:, 3])
    sig_y = list(sig.iloc[:, 4])
    non_x = list(non_sig.iloc[:, 3])
    non_y = list(non_sig.iloc[:, 4])

    for index, value in enumerate(sig_x):
        try:
            sig_x[index] = math.log(value, 10)
        except:
            pass

    for index, value in enumerate(non_x):
        try:
            non_x[index] = math.log(value, 10)
        except:
            pass
    for index, value in enumerate(non_y):
        non_y[index] = (math.log(value, 10)) * -1
    for index, value in enumerate(sig_y):
        sig_y[index] = (math.log(value, 10)) * -1

    sig.iloc[:, 1] = sig_x
    sig.iloc[:, 2] = sig_y
    sig = sig.replace([np.inf, -np.inf], np.nan)
    sig = sig.dropna(axis=0)
    sig = sig.replace(0.000000, np.nan)
    sig = sig.dropna(axis=0)

    non_sig.iloc[:, 1] = non_x
    non_sig.iloc[:, 2] = non_y
    non_sig = non_sig.replace([np.inf, -np.inf], np.nan)
    non_sig = non_sig.dropna(axis=0)
    non_sig = non_sig.replace(0.000000, np.nan)
    non_sig = non_sig.dropna(axis=0)

    TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    # Generating the bokeh figure/plot
    p2 = figure(tools=TOOLS)

    # Plotting our points
    p2.circle(non_sig.iloc[:, 1], non_sig.iloc[:, 2], size=5, fill_color="orange", line_color="green", line_width=1,
             legend_label="Fold change < 100 and > 0.1")
    p2.circle(sig.iloc[:, 1], sig.iloc[:, 2], size=5, fill_color="blue", line_color="green", line_width=1,
             legend_label="Fold change > 100 or < 0.1")
    p2.legend.location = "top_left"
    p2.legend.click_policy = "hide"
    p2.xaxis.axis_label = 'Fold change(log10)'
    p2.yaxis.axis_label = "p-value (log10)"

    # A horizontal line; anything above this line has a sig P-value < 0.05
    hline = Span(location=1.3, dimension='width', line_color='red', line_width=2, line_dash='dashed')
    p2.renderers.extend([hline])

    return (p2)

#KSEA analysis on the table provided by the user (file_to_analyze)
def KSEA_analysis(file_to_analyze, File_location):
    "The file_to_analyze is the data that the user inputs. The File_location is the Kinase-Substrate relation of PhosphositePlus"

    inhibitor_analysis = pd.read_csv(file_to_analyze, sep="\t")

    colnames = inhibitor_analysis.columns[0:]
    inhibitor_name= colnames[2].replace("_mean","")

    df=inhibitor_analysis
    #removing columns that are completely empty
    df=df.dropna(how= "all", axis=1)

    #changing inf and 0 values to NaN to remove them after
    df= df.replace([np.inf, -np.inf], np.nan)

    #removing rows with at least one column empty
    df = df.dropna(axis=0)

    # calculating mean log2 of fold change of all phosphosite in the dataset and the log2(FC) standard deviation
    FC_log = np.log2(df.iloc[: ,3])
    FC_log = FC_log.replace([np.inf, -np.inf], np.nan)
    FC_log = FC_log.dropna(axis=0)
    #standard deviation of all phosphosites fold change(log2)
    SD_phospho= np.std(FC_log)

    FC_log_mean = FC_log.mean()

    #calculating the mean log2(FC) of known phosphosite substrates of the given kinase
    #parsing the input data to have substrate and residue location
    k_sub_loc = df.iloc[: ,0].str.split("(", n=1, expand=True)

    df["Substrates"]= k_sub_loc[0]
    #removing ")" and "_HUMAN" from the residue and substrate
    df["Location"]= k_sub_loc[1].str.replace(")",(""))
    df["Substrates"] = df["Substrates"].str.replace("_HUMAN", "")

    #removing "Substrate" column (first one)
    df= df.drop(df.columns[0], axis=1)


    #Getting the kinase-substrate relation from PhosphositePLUS table
    K_SUB = pd.read_csv(File_location , sep="\t")
    #keepign only rows where the organism is the human
    K_SUB = K_SUB[K_SUB.KIN_ORGANISM == "human"]
    #making all K_SUB uppercase because our dataset is also in uppercase
    K_SUB["SUBSTRATE"]= K_SUB["SUBSTRATE"].str.upper()
    K_SUB["SUB_GENE"]= K_SUB["SUB_GENE"].str.upper()

    #getting kinase and substrate that match the dataset
    #matching subtrates and residue of Phopshoite plus website with our dataset, adding the kinase
    df1 = df.join(K_SUB[["KINASE", "SUBSTRATE", "SUB_MOD_RSD"]].set_index(["SUBSTRATE", "SUB_MOD_RSD"]),
                  on=["Substrates", "Location"])
    #matching GENE substrate and residue of Phopshoite plus website with our dataset, adding the kinase
    df2 = df.join(K_SUB[["KINASE", "SUB_GENE", "SUB_MOD_RSD"]].set_index(["SUB_GENE", "SUB_MOD_RSD"]),
                  on=["Substrates", "Location"])

    df = pd.concat([df1, df2], axis=0)
    df = df.drop_duplicates(keep="first", inplace=False)

    ##droping all rows that have not matched any kinase
    df1 = df.dropna(subset=["KINASE"], axis=0)
    #saving the rows that have not a Matcehd KINASE
    df_all_SUBSTRATES_NO_KINASE = pd.concat([df,df1]).drop_duplicates(keep=False)
    df_all_SUBSTRATES_NO_KINASE = df_all_SUBSTRATES_NO_KINASE.drop("KINASE",1)



    df1=df1.drop_duplicates(keep="first", inplace=False)


    #counting total number of phosphosite substrates identified from the experiment that annotate to the specified kinase
    Grouping_kinases_count= df1.groupby("KINASE").size()
    #print Grouping_kinases_count
    #calculating the square root of each count
    sqrroot_all_kinases= np.sqrt(Grouping_kinases_count)
    #print sqrroot_all_kinases

    FC= np.log2(df1.iloc[: ,2])
    df1["log_FC"] = FC

    FC_Kinases = df1.groupby("KINASE")[["log_FC"]].mean()

    s_p= FC_Kinases - FC_log_mean

    s_px_sqR_m = s_p.mul(sqrroot_all_kinases, axis=0)

    z_score= s_px_sqR_m / SD_phospho
    z_score.reset_index(inplace=True)
    z_score = z_score.replace([np.inf, -np.inf], np.nan)
    z_score = z_score.dropna(axis=0)
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
    output = {'z_score': z_score, "z_score_sig" : z_score_sig, "df_all_SUBSTRATES_NO_KINASE" :df_all_SUBSTRATES_NO_KINASE,
              "inhibitor_name" : inhibitor_name}
    return output

#Creating the two bar plots
def bar_plot(z_score):
    p1 = figure(x_range=z_score["KINASE"],title= " KSEA-based Protein activity", plot_width=1300)
    p1.vbar(x=z_score["KINASE"], top=z_score["z_score"], width=0.9, color = "#ff1200")
    p1.xaxis.major_label_orientation = math.pi/2
    p1.xaxis.axis_label = 'Kinases'
    p1.yaxis.axis_label = "Z-score"
    #output_file("z_Score_bar.html")
    return (p1)
def bar_plot1(z_score_sig):
    # creating barplot with only the significant z_scores
    p = figure(x_range=z_score_sig["KINASE"], title="Protein activity of significant activity changes",
               plot_width=1000)
    p.vbar(x=z_score_sig["KINASE"], top=z_score_sig["z_score"], width=0.5, color="#ff1200")
    p.xaxis.major_label_orientation = math.pi / 2
    p.xaxis.axis_label = 'Kinases'
    p.yaxis.axis_label = "Z-score"
    #show(p)
    return (p)

@app.route("/example")
def example():
    file_path= "/Users/pedromoreno/Downloads/Ipatasertib.tsv"
    file_location = "/Users/pedromoreno/Documents/Kinase_Substrate_Dataset.txt"
    # making the analysis
    KSEA_results= KSEA_analysis(file_path, file_location)
    name= KSEA_results.get("inhibitor_name")
    #Create the plots

    plot = bar_plot(KSEA_results.get("z_score"))
    plot1 = bar_plot1(KSEA_results.get("z_score_sig"))
    plot3 = volcano(file_path)
    #calculating how many susbstrates coul not match a kinase
    Substrates_with_no_kinases = KSEA_results.get("df_all_SUBSTRATES_NO_KINASE")
    amount = Substrates_with_no_kinases["control_mean"].count()
    #volcano plot

    kinase_table= KSEA_results.get("z_score")



    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    script1, div1 = components(plot1)
    script2, div2 = components(plot3)

    return render_template("analysis.html", script=script, div=div, script1=script1, div1=div1, amount = amount,
                           name= name, kinase_table=kinase_table, Substrates_with_no_kinases = Substrates_with_no_kinases,
                           script2=script2, div2=div2)

#start the web server
if __name__ == "__main__":
    app.run(debug=True)
