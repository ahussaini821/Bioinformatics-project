import pandas as pd
import os




#This switch tells us to read data from a csv source or mysql tables. 
iscsv = True


#kinaselisttable is supposedly the name of the table which will contain kinase list data
kinaselisttable = os.path.join(os.getcwd() , 'webapp\\db\\names_final.csv') if iscsv else 'kinaselist'
characteristicstable = os.path.join(os.getcwd() , 'webapp\\db\\characteristics_final.csv') if iscsv else 'characteristics'
domainstable = os.path.join(os.getcwd() , 'webapp\\db\\domains_final.csv') if iscsv else 'domains'
targetstable = os.path.join(os.getcwd() , 'webapp\\db\\kinase target final.csv') if iscsv else 'targets'

'''
def return_row(tablename,filter)

Function used to return data from database/csv files to populate the html pages. If iscsv is True it return data from 
csv files , else it returns data from actual table. The table related code needs to be developed once 
tables are created. 

tablename
    this parameter contains actual table name or path of the csv file
filter
    filter is a list of length 2, where the first item will contain column name and second will be actual value
    of the column on which filter needs to be applied. Holds good for csv files only currently        
'''

def return_row(tablename,filter=None):
    #Read from csv files if it is csv otherwise read tables from database
    if iscsv:
        df = pd.read_csv(tablename)
        if filter :
            df_filtered = df[df[filter[0]].str.match(filter[1])]
            Row_list = df_filtered.values.tolist()
        else :
            Row_list = df.values.tolist()
        return (list(df.columns) , Row_list)
    else :
        pass


def search(option, name):
	if option == 'Protein':
		searchProtein(name)
	if option == 'Kynase':
		pass
	if option == 'Protein':
		pass

#kinase_list.csv
def searchProtein(name):
    return return_row(kinaselisttable , ['Main gene name',name])

def characteristics(name):
    return return_row(characteristicstable , ['Kinase Accession',name])

def domains(name):
    return return_row(domainstable , ['Kinase accession code',name])

def targets(name):
    return return_row(targetstable , ['Target accession',name])


#print(searchProtein("abc"))


