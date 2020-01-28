from webapp import app
from flask import render_template, request
from webapp.dataAccess import searchProtein, characteristics, domains, targets, sequence, inhibitor

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
    header, data = searchProtein(searchString)
    hinhibitor, dinhibitor = inhibitor(searchString)
    if searchCategory == "3":
        return render_template('inhibitorDetails.html', title='Inhibitor Details', header=hinhibitor, data=dinhibitor, search=searchString)
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
    hsequence, dsequence = sequence(accession)
    hsearchProtein, dsearchProtein = searchProtein(searchString)
    return render_template('protein.html', title='Protein Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hdomains=hdomains, ddomains=ddomains, \
        htargets=htargets, dtargets=dtargets, \
        hsequence=hsequence, dsequence=dsequence, \
        hsearchProtein=hsearchProtein, dsearchProtein=dsearchProtein, searchString=searchString)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')