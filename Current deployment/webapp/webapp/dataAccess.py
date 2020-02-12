"""
This file contains all the functions needed to retrieve data from the database
through SQLite queries
"""

import pandas as pd
import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Creates a database connection to the SQLite database
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

# This is a small function which allows protein sequences to be divided into
# blocks of 10
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

"""
The functions below retrive information from the database using a serach query
which could be something such a protein accession or a search string entered
by the user
e.g. get_accession retrieves the accession of a protein or proteins based on a
search query entered by a user
"""
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

def get_inhibitor_alias(conn, cnumber):
    cur = conn.cursor()
    cur.execute("SELECT inhibitor_names.Alias FROM inhibitor_names WHERE inhibitor_names.Cnumber = ?", (cnumber[0][0],))
    rows = cur.fetchall()

    return rows
