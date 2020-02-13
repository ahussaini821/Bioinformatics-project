# Kinview

Kinview is a webapp dedicated to providing information about kinases, their inhibitors, kinase targets and the phosphposites on these kinase targets. The webapp has a number of features including the ability to analyse phosphoproteomics data and give informatin about kianse activity as a well a phosphosite genome browser.

Instructions to use the webapp locally can be found below.

# To use the webapp online
http://kinview-env.p3rqxnfk29.us-west-2.elasticbeanstalk.com/

# To use the webapp on your local machine
Python 3 must be installed to use the webapp on your local machine

Clone the repository

Open terminal and navigate to the directory where you cloned the repository

Run the following commands:

1. python3 -m venv venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. export FLASK_APP = "application.py"
5. flask run


