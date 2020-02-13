from flask import render_template
from webapp import application

@application.errorhandler(404)
def notFoundError(error):
    return render_template('404.html'), 404

@application.errorhandler(500)
def internalError(error):
    return render_template('500.html'), 500
