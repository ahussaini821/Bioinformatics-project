#some code to clean the tables: sequence and  inhibitors (removing columns and making it in the rigth structure
import pandas as pd

data = pd.read_csv("/Users/pedromoreno/inhibitor_kinase_acc.tsv.txt", sep="\t")
print data
##removing column
data= data.drop(["Unnamed: 8"], axis= 1)
#safe it to a new .csv file
data.to_csv('/Users/pedromoreno/inhibitor_kinase_last', index=False, header=True)




##
sequence_data = pd.read_csv("/Users/pedromoreno/Downloads/sequences_final.csv")
##removing column (RNA)
sequence_data = sequence_data.drop(["RNA sequence"], axis= 1)

##removing duplicates
sequence_data.drop_duplicates(subset=None, keep="first", inplace=True)
##saving to a new .csv
sequence_data.to_csv("/Users/pedromoreno/sequence_nodupes_noRNA.csv",index=False, header=True)

##cleaning inhibitor names table
alias_data = pd.read_csv("/Users/pedromoreno/Documents/Bioinformatic group project/Bioinformatics-project/Inhibitor tables/inhibitor_name_database_2.csv", sep=",")
#removing column CAS
alias_data = alias_data.drop(["CAS"], axis= 1)
##removing last row (which is empty)
alias_data = alias_data.iloc[:-1]
print alias_data

##saving to  a new .csv
alias_data.to_csv("/Users/pedromoreno/Alias_final_pedro.csv", index=False)