import os
from webapp import app
from flask import render_template, request, send_file, send_from_directory
from webapp.dataAccess import searchProtein, characteristics, domains, targets, sequence, inhibitor, targetsKAccession

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Maria'}
    posts = [
        {
            'author': {'username': 'Maria'},
            'body': 'Beautiful day!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/searchresults', methods = ['GET', 'POST'])
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
    header, data = searchProtein(searchString.upper())
    hinhibitor, dinhibitor = inhibitor(searchString)
    if searchCategory == "3":
        return render_template('inhibitorresults.html', title='Inhibitor Details', header=hinhibitor, data=dinhibitor, search=searchString)
    else:
        return render_template('searchresults.html', title='Similar Result', header=header, data=data, search=searchString)

@app.route('/kactivityanalysis')
def kActivityAnalysis():
    return render_template('kactivityanalysis.html', title='Kinases Activity Analysis')

@app.route('/protein')
def protein():
    searchString = ""
    accession = ""
    if request.args :
        searchString =  request.args['searchString']
        accession = request.args['accession']
    hcharacteristics, dcharacteristics = characteristics(accession)
    hdomains, ddomains = domains(accession)
    htargets, dtargets = targets(accession)
    htargetsKAccess, dtargetsKAccess = targetsKAccession(accession)
    hsequence, dsequence = sequence(accession)
    hsearchProtein, dsearchProtein = searchProtein(searchString)
    return render_template('protein.html', title='Protein Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hdomains=hdomains, ddomains=ddomains, \
        htargets=htargets, dtargets=dtargets, \
        hsequence=hsequence, dsequence=dsequence, \
        hsearchProtein=hsearchProtein, dsearchProtein=dsearchProtein, \
        htargetsKAccess=htargetsKAccess, dtargetsKAccess=dtargetsKAccess, searchString=searchString)

@app.route('/inhibitor')
def inhibitorDetails():
    searchInhibitor = ""
    if request.args :
        searchInhibitor =  request.args['searchInhibitor']
    hinhibitor, dinhibitor = inhibitor(searchInhibitor)
    structureImgName = str(dinhibitor[0][0]) + '.png' 
    return render_template('inhibitor.html', title='Inhibitor Details', \
        hinhibitor=hinhibitor, dinhibitor=dinhibitor, searchInhibitor=searchInhibitor, structureImgName=structureImgName)

@app.route('/sequencedownload')
def sequenceDownload():
    return send_from_directory(os.path.join(os.getcwd(),'webapp/db/xnvjcv.csv'), 'proteinjjfgjffinal.csv', as_attachment=True)
    #return send_file('./db/protein_final.csv',as_attachment=True, attachment_filename='protein_final.csv')


@app.route('/chromosome')
def genomeBrowser():
    chromosomes = ["Chromosome 1", "Chromosome 2", "Chromosome 3", "Chromosome 4", "Chromosome 5", "Chromosome 6",
    "Chromosome 7", "Chromosome 8", "Chromosome 9", "Chromosome 10", "Chromosome 11", "Chromosome 12",
    "Chromosome 13", "Chromosome 14", "Chromosome 15", "Chromosome 16", "Chromosome 17", "Chromosome 18",
    "Chromosome 19", "Chromosome 20", "Chromosome 21", "Chromosome 22", "Chromosome X", "Chromosome Y",]
    return render_template('chromosomes.html', title="Chromosome", chromosomes=chromosomes)

@app.route('/chromosomedetails')
def genomeDetails():
    chromosome = ""
    if request.args :
        chromosome =  request.args['chromosome']
    return render_template(chromosome+'.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')