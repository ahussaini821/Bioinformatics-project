from webapp import app
from flask import render_template, request
from webapp.dataAccess import searchProtein, characteristics, domains, targets

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
    if request.method == 'POST':
        formData = request.form.items()
        for key, value in formData:
            if key == "searchString":
                searchString = value
    header, data = searchProtein(searchString)
    return render_template('searchresults.html', title='Similar Result', header=header, data=data, search=searchString)

@app.route('/kactivityanalysis')
def kActivityAnalysis():
    return render_template('kactivityanalysis.html', title='Kinases Activity Analysis')

@app.route('/protein')
def protein():
    hcharacteristics, dcharacteristics = characteristics("")
    hdomains, ddomains = domains("")
    htargets, dtargets = targets("")
    return render_template('protein.html', title='Protein Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hdomains=hdomains, ddomains=ddomains, \
        htargets=htargets, dtargets=dtargets)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')