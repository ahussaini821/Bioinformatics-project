import os
from webapp import application
from flask import render_template, request, send_file, send_from_directory
from flask import Flask, flash, request, redirect, url_for
from webapp.dataAccess import get_accession, get_characteristics, get_domains, get_targets, get_phosphosites, get_names, get_inhibitors, is_kinase, is_substrate
from webapp.dataAccess import get_inhibitors_cnumber, get_inhibitors_info, divider, get_sequence, get_inhibitor_alias, create_connection
from werkzeug.utils import secure_filename
from webapp.analysis import KSEA_analysis, bar_plot, bar_plot1, volcano, normpdf, remove_empty, element
import pandas as pd
import numpy as np
import math
from math import pi
from lib2to3.fixer_util import p2
from bokeh.command.util import set_single_plot_width_height
from bokeh.document import Document
from bokeh.embed import components, file_html
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot
from bokeh.models import (Circle, ColumnDataSource, Div, Grid, Line,
                          LinearAxis, Plot, Range1d, Span)
from bokeh.palettes import Category20c, GnBu3, OrRd3
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
from bokeh.sampledata.autompg import autompg
from bokeh.transform import cumsum, jitter
from bokeh.util.browser import view
from bokeh.util.string import encode_utf8


"""
Below are the various pages of the website
"""
@application.route('/')

@application.route('/index')
def index():
    user = {'username': 'Maria'}
    posts = [
        {
            'author': {'username': 'Maria'},
            'body': 'Beautiful day!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


# A function for limiting the file types allowed to upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'tsv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    filename = ''
    if request.method == 'POST':

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('results',
                                    filename=filename))
    return render_template('uploads.html', title="Kinase activity analysis", filename=filename)

@application.route('/results/<filename>', methods=['GET', 'POST'])
def results(filename):

    file_path = 'webapp/cache/' + filename
    file_location = 'webapp/cache/kinase_substrate_PHOSPHO.tsv'
    KSEA_results= KSEA_analysis(file_path, file_location)
    name= KSEA_results.get("inhibitor_name")

    # Create the plots
    plot = bar_plot(KSEA_results.get("z_score"))
    plot1 = bar_plot1(KSEA_results.get("z_score_sig"))
    plot3 = volcano(file_path)

    # Calculating how many susbstrates coul not match a kinase
    Substrates_with_no_kinases = KSEA_results.get("df_all_SUBSTRATES_NO_KINASE")
    amount = Substrates_with_no_kinases["control_mean"].count()

    # Volcano plot
    kinase_table= KSEA_results.get("z_score")

    script_yuting, div_yuting=element(file_path)

    # Grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    script1, div1 = components(plot1)
    script2, div2 = components(plot3)

    return render_template("results.html",
        plot_script=script_yuting,plot_div=div_yuting,js_resources=js_resources,css_resources=css_resources,


        script=script, div=div, script1=script1, div1=div1, amount = amount,name= name, kinase_table=kinase_table, Substrates_with_no_kinases = Substrates_with_no_kinases,script2=script2, div2=div2)





@application.route('/searchresults', methods = ['GET', 'POST'])
def searchResults():
    searchString = ""
    searchCategory = "1"
    if request.method == 'POST':
        formData = request.form.items()
        for key, value in formData:
            if key == "searchString":
                searchString = value
            if key == "selectSearchCategory":
                searchCategory = value
    header = ['Accession', 'Main gene name', 'Main protein name', 'Other gene names', 'Other protein names']
    hinhibitor = ['CNumber', 'Inhibitor', 'Molecular Formula', 'Molecular Weight', 'target', 'other target', 'Reference 1', 'Reference 2', 'SMILES']

    searchString2 = "%" + searchString.upper() + "%"

    conn = create_connection("webapp/db/kinase.db")
    data = []

    if searchCategory == "3":
        cnumbers = get_inhibitors_cnumber(conn, searchString2)
        for i in cnumbers:
            curr_data = get_inhibitors_info(conn,i[0])
            data += curr_data

        dinhibitor = data
        print(dinhibitor[0][0])
        img_name = str(dinhibitor[0][0]) + '.png'

        return render_template('inhibitorresults.html', title='Inhibitor Details', header=hinhibitor, data=dinhibitor, search=searchString, img_name=img_name)
    elif searchCategory == "1":
        accessions = get_accession(conn, searchString2)
        for accession in accessions:
            kinase_exists = is_kinase(conn, accession[0])
            if kinase_exists:
                data += get_names(conn, accession[0])
            else:

                continue

        return render_template('searchresults.html', title='Similar Result', header=header, data=data, search=searchString)
    elif searchCategory == "2":
        accessions = get_accession(conn, searchString2)
        for accession in accessions:
            substrate_exists = is_substrate(conn, accession[0])
            if substrate_exists:
                data += get_names(conn, accession[0])
            else:
                continue

        return render_template('substrateresults.html', title='Similar Result', header=header, data=data, search=searchString)


@application.route('/protein')
def protein():
    # These are the headings of the column names used in the tables of the
    # website
    hdomains = ['Kinase accession code', 'Domain', 'Domain position']
    hcharacteristics = ['Kinase Accession', 'Family', 'Subcellular location']
    htargets = ['Kinase accession', 'Target accession', 'Location', 'Chromosome', 'Start', 'End', 'Phosphosite position', 'Neighbouring amino sequences']
    htargetsKAccess = ['Kinase accession', 'Target accession', 'Location', 'Chromosome', 'Start', 'End', 'Phosphosite position', 'Neighbouring amino sequences']
    hsequence = ['Accession', 'DNA sequence', 'Protein sequence', 'RNA sequence', 'Transcript ID']
    hsearchProtein = ['Accession', 'Main gene name', 'Main protein name', 'Other gene names', 'Other protein names']
    hphosphosites = ["Kinase", "Location", "Chromosome", "Start", "End"]
    hinhibitor = ["Inhibitor name", "C Number", "Molecular weight"]

    conn = create_connection("webapp/db/kinase.db")

    searchString = ""
    accession = ""
    if request.args :
        searchString =  request.args['searchString']
        accession = request.args['accession']

    dcharacteristics = get_characteristics(conn,accession)
    ddomains = get_domains(conn,accession)
    dtargets = get_targets(conn,accession)
    dphosphosites = get_phosphosites(conn,accession)
    dnames = get_names(conn,accession)
    accession2 = "%" + accession + "%"
    dinhibitors = get_inhibitors(conn,accession,accession2)
    dsequence = get_sequence(conn,accession)
    new_targets = []
    targetnames2 = []

    for index,i in enumerate(dtargets):
        targetnames2.append(get_names(conn,i[0]))
    try:
        targetnames = targetnames2[0]
    except:
        targetnames = [()]

    sequence = divider(dsequence[0][1])

    return render_template('protein.html', title='Protein Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hdomains=hdomains, ddomains=ddomains, \
        htargets=htargets, dtargets=dtargets, targetnames=targetnames, \
        hsequence=hsequence, dsequence=dsequence, sequence=sequence, \
        hsearchProtein=hsearchProtein, dsearchProtein=dnames, \
        htargetsKAccess=htargetsKAccess, dtargetsKAccess=dtargets, searchString=searchString, \
        hphosphosites=hphosphosites, dphosphosites=dphosphosites, \
        hinhibitor=hinhibitor, dinhibitors=dinhibitors, accession=accession)

@application.route('/inhibitor')
def inhibitorDetails():
    conn = create_connection("webapp/db/kinase.db")
    searchInhibitor = ""

    if request.args :
        searchInhibitor =  request.args['searchInhibitor']

    hinhibitor = ["Inhibitor name", "Molecular formula", "Molecular weight", "Main target accession", "Other targets", "Reference 1", "Reference 2", "SMILES formula"]
    searchInhibitor2 = "%" + searchInhibitor + "%"
    cnumbers = get_inhibitors_cnumber(conn, searchInhibitor)
    data = []
    alias = get_inhibitor_alias(conn, cnumbers)
    try:
        alias = alias[0][0]
    except:
        alias=""

    for i in cnumbers:
        curr_data = get_inhibitors_info(conn,i[0])
        data += curr_data

    dinhibitor = data
    structureImgName = str(dinhibitor[0][0]) + '.png'
    return render_template('inhibitor.html', title='Inhibitor Details', \
        hinhibitor=hinhibitor, dinhibitor=dinhibitor, searchInhibitor=searchInhibitor, structureImgName=structureImgName,alias=alias)

@application.route('/sequencedownload')
def sequenceDownload():
    return send_from_directory(os.path.join(os.getcwd(),'webapp/db/xnvjcv.csv'), 'proteinjjfgjffinal.csv', as_attachment=True)


@application.route('/substrate')
def substrate():

    htargetsKAccess = ['Kinase accession', 'Target accession', 'Location', 'Chromosome', 'Start', 'End', 'Phosphosite position', 'Neighbouring amino sequences']
    hsequence = ['Accession', 'DNA sequence', 'Protein sequence', 'RNA sequence', 'Transcript ID']
    hsearchProtein = ['Accession', 'Main gene name', 'Main protein name', 'Other gene names', 'Other protein names']
    hphosphosites = ["Kinase", "Location", "Chromosome", "Start", "End"]
    htargets = ['Kinase accession', 'Target accession', 'Location', 'Chromosome', 'Start', 'End', 'Phosphosite position', 'Neighbouring amino sequences']

    conn = create_connection("webapp/db/kinase.db")

    searchString = ""
    accession = ""
    if request.args :
        searchString =  request.args['searchString']
        accession = request.args['accession']

    dtargets = get_targets(conn,accession)
    dphosphosites = get_phosphosites(conn,accession)
    dnames = get_names(conn,accession)
    dtargets = get_targets(conn,accession)
    dsequence = get_sequence(conn,accession)

    """
    Dividing the sequence into blocks of 10
    and also changing the residues which are Phosphosites to lowercase
    """
    sequence = dsequence[0][1]
    list_sequence = list(sequence)
    for i in dphosphosites:
        curr_res = i[1]
        curr_pos = curr_res[1:]
        list_sequence[int(curr_pos)-1] = list_sequence[int(curr_pos)-1].lower()

    sequence = ''.join(list_sequence)
    sequence = divider(sequence)

    return render_template('substrate.html', title='Substrate Details', \
        htargets=htargets, dtargets=dtargets, \
        hsequence=hsequence, dsequence=dsequence, sequence=sequence, \
        hsearchProtein=hsearchProtein, dsearchProtein=dnames, \
        htargetsKAccess=htargetsKAccess, dtargetsKAccess=dtargets, searchString=searchString, \
        hphosphosites=hphosphosites, dphosphosites=dphosphosites, accession=accession)

@application.route('/genomebrowser')
def genomeBrowser():
    return render_template('genomebrowser.html', title='Genome browser')

@application.route('/about')
def about():
    return render_template('about.html', title='About Us')

@application.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')
