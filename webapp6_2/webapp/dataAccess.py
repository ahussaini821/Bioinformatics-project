import pandas as pd
import os




# This switch tells us to read data from a csv source or mysql tables. 
iscsv = True
# Database details , put this in a config file afterwards
v_host="localhost"
v_user="root"
v_passwd="44Gt66pa"
v_port=""
v_database = "kinase_db"


# kinaselisttable is supposedly the name of the table which will contain kinase list data
kinaselisttable = os.path.join(os.getcwd() , 'webapp/db/names_final.csv') if iscsv else 'Protein'
characteristicstable = os.path.join(os.getcwd() , 'webapp/db/characteristics_final.csv') if iscsv else 'kinase_characteristics'
domainstable = os.path.join(os.getcwd() , 'webapp/db/domains_final.csv') if iscsv else 'domains'
targetstable = os.path.join(os.getcwd() , 'webapp/db/kinase target final.csv') if iscsv else 'kinase_targets'
sequencestable = os.path.join(os.getcwd() , 'webapp/db/sequences_final.csv') if iscsv else 'sequences'
inhibitortable = os.path.join(os.getcwd() , 'webapp/db/inhibitor_final.csv') if iscsv else 'inhibitor'

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

def return_row(tablename,filterc=None):
    # Read from csv files if it is csv otherwise read tables from database
    if iscsv:
        df = pd.read_csv(tablename)
        if filterc :
            df_filtered = df[df[filterc[0]].str.match(filterc[1])]
            Row_list = df_filtered.values.tolist()
        else :
            Row_list = df.values.tolist()
        return (list(df.columns) , Row_list)
    else :
        import mysql.connector
        mydb = mysql.connector.connect(host=v_host,user=v_user,passwd=v_passwd,port = v_port,database =v_database)
        mycur = mydb.cursor()
        sql = 'select * from {tab} {where} '.format(tab=tablename,where='where' if filterc else '')
        if filterc :
            sql = sql + "{col} like '{val}%'".format(col=filterc[0],val=filterc[1])
        print (sql)
        mycur.execute(sql)
        field_names = [i[0] for i in mycur.description]
        retval =  (field_names , list(mycur.fetchall()))
        mycur.close()
        mydb.close()
        return retval



def search(option, name):
	if option == 'Protein':
		searchProtein(name)
	if option == 'Kynase':
		pass
	if option == 'Protein':
		pass

# kinase_list.csv
def searchProtein(name):
    return return_row(kinaselisttable , ['gene_name',name])

def characteristics(name):
    return return_row(characteristicstable , ['accession_number',name])

def domains(name):
    return return_row(domainstable , ['accession_number',name])

def targets(name):
    return return_row(targetstable , ['T_accession_number',name])

def sequence(name):
    return return_row(sequencestable , ['Accession',name])

def inhibitor(name):
    return return_row(inhibitortable , ['Target',name])


