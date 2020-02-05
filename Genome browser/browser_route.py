@application.route('/genomebrowser')
def genomebrowser():
    return render_template('genomebrowser.html', title='Genome browser')
