#Import the dependencies that we will be using in this file
import pandas as pd
import os


#This switch tells us to read data from a csv source or mysql tables. 
iscsv = True


#Setting up the data tables based upon 'iscsv' flag!
kinaselisttable = os.path.join(os.getcwd() , 'webapp/db/protein_final.csv') if iscsv else 'kinaselist'
characteristicstable = os.path.join(os.getcwd() , 'webapp/db/kinase_characteristics_final.csv') if iscsv else 'characteristics'
domainstable = os.path.join(os.getcwd() , 'webapp/db/domains_final.csv') if iscsv else 'domains'
targetstable = os.path.join(os.getcwd() , 'webapp/db/kinase target final no na.csv') if iscsv else 'targets'
sequencestable = os.path.join(os.getcwd() , 'webapp/db/sequences_final.csv') if iscsv else 'sequences'
inhibitortable = os.path.join(os.getcwd() , 'webapp/db/kinase_inhibitors_final.csv') if iscsv else 'inhibitor'


"""[Description]
    def return_row(tablename,filter)

    Function used to return data from database/csv files to populate the html pages. If iscsv is True it return data from 
    csv files , else it returns data from actual table. The table related code needs to be developed once 
    tables are created. 

    tablename
        this parameter contains actual table name or path of the csv file
    filter
        filter is a list of length 2, where the first item will contain column name and second will be actual value
        of the column on which filter needs to be applied. Holds good for csv files only currently        
"""
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


""" [Description]
    Function is used to search the Protein From Kinase table, and if there is a match,
    it search in Characteristic table.
    'A valid protein should have entry in both the places.' 
    
    Arguments:
        name {[str]} -- The string to be searched in Kinase Table (Needs to be in Upper Case)
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def searchProtein(name):
    row_list = []
    head, data = return_row(kinaselisttable , ['Main protein name',name])
    for row in data:
        if (row[0]):
            d = return_row(characteristicstable , ['Kinase Accession',row[0]])
            if (len(d[1]) > 0):
                row_list.append(row)
    return (head, row_list)


""" [Description]
    Function is used to search the Substrate From Kinase table, and if there is a match,
    it search in Characteristic table.
    'A valid Substrate should have entry in both the places.' 
    
    Arguments:
        name {[str]} -- The string to be searched in Kinase Table
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def searchSubstrate(name):
    row_list = []
    head, data_gene = return_row(kinaselisttable , ['Main gene name',name.upper()])
    if len(data_gene) > 0:
        for row in data_gene:
            if (row[0]):
                d = return_row(characteristicstable , ['Kinase Accession',row[0]])
                if (len(d[1]) > 0):
                    row_list.append(row)
    head, data_protein = return_row(kinaselisttable , ['Main protein name',name.upper()])
    if len(data_protein) > 0:
        for row in data_protein:
            if (row[0]):
                d = return_row(characteristicstable , ['Kinase Accession',row[0]])
                if (len(d[1]) > 0):
                    row_list.append(row)
    return (head, row_list)


""" [Description]
    Function is used to search the Gene From Kinase table.
    
    Arguments:
        name {[str]} -- The string to be searched in Kinase Table (Needs to be in Upper Case)
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def searchGene(name):
    return return_row(kinaselisttable , ['Main gene name',name])


""" [Description]
    Function is used to search the accession From characteristics table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def characteristics(name):
    return return_row(characteristicstable , ['Kinase Accession',name])


""" [Description]
    Function is used to search the accession From Domains table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def domains(name):
    return return_row(domainstable , ['Kinase accession code',name])


""" [Description]
    Function is used to search the accession From Targets table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def targets(name):
    return return_row(targetstable , ['Target accession',name])


""" [Description]
    Function is used to search the Kinase Accession From Targets table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def targetsKAccession(name):
    return return_row(targetstable , ['Kinase accession',name])


""" [Description]
    Function is used to search the Kinase Accession From Sequence table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def sequence(name):
    return return_row(sequencestable , ['Accession',name])


""" [Description]
    Function is used to search the Inhibitor name From Inhibitor table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def inhibitor(name):
    return return_row(inhibitortable , ['Inhibitor',name])


""" [Description]
    Function is used to search the Accession From Inhibitor table.
    
    Arguments:
        name {[str]} -- The string to be searched.
    
    Returns:
        [tuple] -- Two lists inside a tuple, one for the headers and other for the data.
"""
def inhibitorAccession(name):
    return return_row(inhibitortable , ['target',name])
