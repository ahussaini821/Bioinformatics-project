#Import the dependencies that we will be using in this file
import os
from webapp import app
from flask import render_template, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from webapp.dataAccess import searchProtein, searchGene, searchSubstrate, inhibitor
from webapp.dataAccess import characteristics, domains, targets, sequence, targetsKAccession, inhibitorAccession
#from webapp.KSEA_analysis import KSEA_analysis, bar_plot, bar_plot1, volcano, components


ALLOWED_EXTENSIONS = {'tsv'}
"""[summary]
    Function to check if the file being uploaded is valid or not?
    It should be one of the files from extension set to process further.

    Arguments:
        filename {[str]} -- Name of the file being uploaded to the server.

    Returns:
        [boolean] -- If the file is valid or not?
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""[summary]
    Route definition for index page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- The template for index page.
"""
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


"""[summary]
    Route definition for Search Results page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- Based upon the search category, different templates are being rendered.
            For Kianese and Gene search -- searchresults.html is rendered with related data.
            For Inhibitor search -- inhibitorresults.html is rendered with related data.
            For Substrate search -- substrateresults.html is rendered with related data.
"""
@app.route('/searchresults', methods = ['GET', 'POST'])
def searchResults():
    searchString = ""
    searchCategory = "1"

    # If a post request, get the form field values for Search Query and Category
    if request.method == 'POST':
        formData = request.form.items()
        for key, value in formData:
            if key == "searchString":
                searchString = value
            if key == "selectSearchCategory":
                searchCategory = value

    # Based on the category, query database and render the results on template
    if searchCategory == "1":
        hkinase, dkinase = searchProtein(searchString.upper())
        return render_template('searchresults.html', title='Kinase Details', header=hkinase, data=dkinase, search=searchString)
    elif searchCategory == "3":
        hinhibitor, dinhibitor = inhibitor(searchString)
        return render_template('inhibitorresults.html', title='Inhibitor Details', header=hinhibitor, data=dinhibitor, search=searchString)
    elif searchCategory == "4":
        hsubstrate, dsubstrate = searchSubstrate(searchString)
        return render_template('substrateresults.html', title='Substrate Details', hsubstrate=hsubstrate, dsubstrate=dsubstrate, search=searchString)
    else:
        header, data = searchGene(searchString.upper())
        return render_template('searchresults.html', title='Similar Result', header=header, data=data, search=searchString)


"""[summary]
    Route definition for File Upload page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- fileupload.html with error message if any, else kActivityAnalysis,html.
"""
@app.route('/fileUpload', methods=['GET', 'POST'])
def kActivityFileUpload():
    status = ''

    # If a file has been uploaded
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            status = 'No file part'
        file = request.files['file']

        # If no file was selected, return error message
        if file.filename == '':
            status = "No selected file"

        # If not in allowed file format, return error message
        if not allowed_file(file.filename):
            status = "File format not supported."

        # If everything is ok, save the file to server and call kActivityAnalysis() for proccessing it.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FILE_PATH'], filename))
            status = "File Uploaded Successfully...!!!"
            return redirect(url_for('kActivityAnalysis', filename=filename))
    return render_template('fileupload.html', title='File Upload', status=status)


"""[summary]
    Route definition for Kinase Activity Analysis page in web application.

    Arguments:
        filename [{str}] -- The Complete path of the file at server.

    Returns:
        [render_template] -- kactivityanalysis.html with the graphs and table.
"""
@app.route('/kactivityanalysis/<filename>')
def kActivityAnalysis(filename):
    # Get the path of files to process
    file_path = os.path.join(app.config['UPLOAD_FILE_PATH'], filename)
    file_location = os.path.join(os.getcwd() , 'webapp/db/kinase_substrate_PHOSPHO')

    # Making the analysis
    KSEA_results= KSEA_analysis(file_path, file_location)
    name= KSEA_results.get("inhibitor_name")

    # Create the plots
    plot = bar_plot(KSEA_results.get("z_score"))
    plot1 = bar_plot1(KSEA_results.get("z_score_sig"))
    plot3 = volcano(file_path)

    #Calculating how many susbstrates coul not match a kinase
    Substrates_with_no_kinases = KSEA_results.get("df_all_SUBSTRATES_NO_KINASE")
    amount = Substrates_with_no_kinases["control_mean"].count()

    #volcano plot
    kinase_table= KSEA_results.get("z_score")

    #getting z_score values
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    script1, div1 = components(plot1)
    script2, div2 = components(plot3)

    return render_template('kactivityanalysis.html', title='Kinases Activity Analysis', \
        script=script, div=div, script1=script1, div1=div1, amount = amount, \
        name= name, kinase_table=kinase_table, Substrates_with_no_kinases = Substrates_with_no_kinases, \
        script2=script2, div2=div2)


"""[summary]
    Route definition for Protein Details page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- protein.html with data to be displayed in each tab.
            hcharacteristics, dcharacteristics  - Characteristics Tab - Selected by default
            hdomains, ddomains                  - Domains Tab
            htargets, dtargets                  - Phosphosites Tab
            htargetsKAccess, dtargetsKAccess    - Targets Tab
            hsequence, dsequence                - Sequence Tab
            hinhibitor, dinhibitor              - Inhibitor Tab
"""
@app.route('/protein')
def protein():
    searchString = ""
    accession = ""

    # Get the values for query params of GET method to the page
    if request.args :
        searchString =  request.args['searchString']
        accession = request.args['accession']

    # Build up the variables to be passed to protein.html for details
    hcharacteristics, dcharacteristics = characteristics(accession)
    hdomains, ddomains = domains(accession)
    htargets, dtargets = targets(accession)
    htargetsKAccess, dtargetsKAccess = targetsKAccession(accession)
    hsequence, dsequence = sequence(accession)
    hinhibitor, dinhibitor = inhibitorAccession(accession)
    hsearchProtein, dsearchProtein = searchProtein(searchString)

    return render_template('protein.html', title='Protein Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hdomains=hdomains, ddomains=ddomains, \
        htargets=htargets, dtargets=dtargets, \
        hsequence=hsequence, dsequence=dsequence, \
        hsearchProtein=hsearchProtein, dsearchProtein=dsearchProtein, \
        hinhibitor=hinhibitor, dinhibitor=dinhibitor, \
        htargetsKAccess=htargetsKAccess, dtargetsKAccess=dtargetsKAccess, searchString=searchString)


"""[summary]
    Route definition for Inhibitor Details page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- inhibitor.html with data to be displayed.
"""
@app.route('/inhibitor')
def inhibitorDetails():
    searchInhibitor = ""

    # Get the values for query params of GET method to the page
    if request.args :
        searchInhibitor =  request.args['searchInhibitor']

    # Get the inhibitor details from databse
    hinhibitor, dinhibitor = inhibitor(searchInhibitor)

    # Build the image name based upon the CNumber
    structureImgName = str(dinhibitor[0][0]) + '.png'

    return render_template('inhibitor.html', title='Inhibitor Details', \
        hinhibitor=hinhibitor, dinhibitor=dinhibitor, searchInhibitor=searchInhibitor, structureImgName=structureImgName)


"""[summary]
    Route definition for Substrate Details page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- substrate.html with data to be displayed in each tab.
            hcharacteristics, dcharacteristics  - Characteristics Tab - Selected by default
            htargets, dtargets                  - Phosphosites Tab
            hsequence, dsequence                - Sequence Tab
"""
@app.route('/substrate')
def substrate():
    searchString = ""
    accession = ""

    # Get the values for query params of GET method to the page
    if request.args :
        searchString =  request.args['searchString']
        accession = request.args['accession']

    # Build up the variables from db methods to be passed to protein.html for details
    hcharacteristics, dcharacteristics = characteristics(accession)
    hsearchProtein, dsearchProtein = searchProtein(searchString)
    htargets, dtargets = targets(accession)
    hsequence, dsequence = sequence(accession)

    return render_template('substrate.html', title='Substrate Details', \
        hcharacteristics=hcharacteristics, dcharacteristics=dcharacteristics, \
        hsearchProtein=hsearchProtein, dsearchProtein=dsearchProtein, \
        htargets=htargets, dtargets=dtargets, \
        hsequence=hsequence, dsequence=dsequence, \
        searchString=searchString)


"""[summary]
    Route definition for Genome Browser page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- chromosomes.html with data to be displayed.
"""
@app.route('/chromosome')
def genomeBrowser():
    # A list of all the available chromosomes
    chromosomes = ["Chromosome 1", "Chromosome 2", "Chromosome 3", "Chromosome 4", "Chromosome 5", "Chromosome 6",
    "Chromosome 7", "Chromosome 8", "Chromosome 9", "Chromosome 10", "Chromosome 11", "Chromosome 12",
    "Chromosome 13", "Chromosome 14", "Chromosome 15", "Chromosome 16", "Chromosome 17", "Chromosome 18",
    "Chromosome 19", "Chromosome 20", "Chromosome 21", "Chromosome 22", "Chromosome X", "Chromosome Y",]

    return render_template('chromosomes.html', title="Chromosome", chromosomes=chromosomes)


"""[summary]
    Route definition for Chromosome Details page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- chromosome<number>.html with data to be displayed.
"""
@app.route('/chromosomedetails')
def genomeDetails():
    chromosome = ""

    # Get the selected chromosome
    if request.args :
        chromosome =  request.args['chromosome']

    return render_template(chromosome+'.html')


"""[summary]
    Route definition for About Us page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- about.html with data to be displayed.
"""
@app.route('/about')
def about():

    return render_template('about.html', title='About Us')


"""[summary]
    Route definition for About Us page in web application.

    Arguments:
        NA

    Returns:
        [render_template] -- about.html with data to be displayed.
"""
@app.route('/contact')
def contact():

    return render_template('contact.html', title='Contact Us')
