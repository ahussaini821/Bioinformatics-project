import pandas as pd
import os
import sqlite3
from sqlite3 import Error

#This switch tells us to read data from a csv source or mysql tables.
iscsv = False

#kinaselisttable is supposedly the name of the table which will contain kinase list data
kinaselisttable = os.path.join(os.getcwd() , 'webapp/db/protein_final.csv') if iscsv else 'kinaselist'
characteristicstable = os.path.join(os.getcwd() , 'webapp/db/kinase_characteristics_final.csv') if iscsv else 'characteristics'
domainstable = os.path.join(os.getcwd() , 'webapp/db/domains_final.csv') if iscsv else 'domains'
targetstable = os.path.join(os.getcwd() , 'webapp/db/kinase target final no na.csv') if iscsv else 'targets'
sequencestable = os.path.join(os.getcwd() , 'webapp/db/sequences_final.csv') if iscsv else 'sequences'
inhibitortable = os.path.join(os.getcwd() , 'webapp/db/kinase_inhibitors_final.csv') if iscsv else 'inhibitor'
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
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    if not conn:
        print("Database not connected?")

    return conn

def divider(string):
    split_string = []
    x = []
    for index in range(0, len(string),10):
        split_string.append(string[index:index+10])
        count=1
    for i in range(0,len(split_string),4):
        curr=count*10
        try:

            x.append(split_string[i]+ " " + split_string[i+1] + " " + split_string[i+2] + " " + split_string[i+3])
        except:
            continue
        count += 4
    y = ""
    for i in x:
        y += i + "\n"

    return(y)



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
def is_kinase(conn, accession):
    cur=conn.cursor()
    cur.execute("SELECT kinase_characteristics.accession_number FROM kinase_characteristics WHERE kinase_characteristics.accession_number = ?", (accession,))
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True

def is_substrate(conn, accession):
    cur=conn.cursor()
    cur.execute("SELECT kinase_targets.T_accession_number FROM kinase_targets WHERE kinase_targets.T_accession_number = ?", (accession,))
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def get_accession(conn, priority):

    cur = conn.cursor()
    cur.execute("SELECT Protein.accession_number FROM Protein WHERE Protein.accession_number LIKE ? OR Protein.gene_name LIKE ? OR Protein.protein_name LIKE ? OR Protein.gene_alias LIKE ? OR Protein.protein_alias LIKE ?", (priority,priority,priority,priority,priority,))
    rows = cur.fetchall()

    return rows

def get_domains(conn,query):

    cur = conn.cursor()
    cur.execute("SELECT domains.accession_number, domains.domain, domains.domain_position FROM domains WHERE domains.accession_number = ?",(query,))

    rows = cur.fetchall()

    return rows

def get_targets(conn,query):

    cur = conn.cursor()
    cur.execute("SELECT kinase_targets.T_accession_number, kinase_targets.phosphosite, kinase_targets.chromosome, kinase_targets.chro_start, kinase_targets.chro_end FROM kinase_targets WHERE kinase_targets.K_accession_number = ?",(query,))

    rows = cur.fetchall()

    return rows

def get_sequence(conn,query):

    cur = conn.cursor()
    cur.execute("SELECT sequence.* FROM sequence WHERE sequence.accession_number = ?",(query,))

    rows = cur.fetchall()

    return rows

def get_phosphosites(conn,query):

    cur = conn.cursor()
    cur.execute("SELECT kinase_targets.K_accession_number, kinase_targets.phosphosite, kinase_targets.chromosome, kinase_targets.chro_start, kinase_targets.chro_end FROM kinase_targets WHERE kinase_targets.T_accession_number = ?",(query,))

    rows = cur.fetchall()

    return rows

def get_names(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT Protein.* FROM Protein WHERE Protein.accession_number = ?", (priority,))

    rows = cur.fetchall()

    return rows

def get_characteristics(conn, query):

    cur = conn.cursor()
    cur.execute("SELECT kinase_characteristics.accession_number, kinase_characteristics.family, kinase_characteristics.cell_location FROM kinase_characteristics WHERE kinase_characteristics.accession_number = ?", (query,))

    rows = cur.fetchall()

    return rows

def get_inhibitors(conn, query,query2):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT kinase_inhibitors.inhibitor, kinase_inhibitors.Cnumber, kinase_inhibitors.Mol_weigth FROM kinase_inhibitors WHERE kinase_inhibitors.other_targets LIKE ? OR kinase_inhibitors.target = ?", (query2,query,))

    rows = cur.fetchall()

    return rows

def get_inhibitors_cnumber(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT inhibitor_names.Cnumber FROM inhibitor_names WHERE inhibitor_names.Alias LIKE ?", (query,))
    rows=cur.fetchall()
    cur.execute("SELECT kinase_inhibitors.Cnumber from kinase_inhibitors WHERE kinase_inhibitors.inhibitor LIKE ?", (query,) )
    rows += cur.fetchall()


    return rows

def get_inhibitors_info(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT kinase_inhibitors.* FROM kinase_inhibitors WHERE kinase_inhibitors.Cnumber = ?", (query,))
    rows=cur.fetchall()

    return rows

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

def targetsKAccession(name):
    return return_row(targetstable , ['Kinase accession',name])

def sequence(name):
    return return_row(sequencestable , ['Accession',name])

def inhibitor(name):

    return return_row(inhibitortable , ['Inhibitor',name])


#print(searchProtein("abc"))
