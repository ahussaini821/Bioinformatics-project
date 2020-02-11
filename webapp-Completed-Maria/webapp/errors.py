#Import the dependencies that we will be using in this file
from flask import render_template
from webapp import app


"""[summary]
    Route definition for '404 - Not Found' error in web application.
    
    Arguments:
        error {[int]} -- the error code from web application.
    
    Returns:
        [render_template] -- The template to handle 404 error.
"""
@app.errorhandler(404)
def notFoundError(error):
    return render_template('404.html'), 404


"""[summary]
    Route definition for '500 - Internal Server Error' in web application.
    
    Arguments:
        error {[int]} -- the error code from web application.
    
    Returns:
        [render_template] -- The template to handle 500 error.
"""
@app.errorhandler(500)
def internalError(error):
    return render_template('500.html'), 500