from webapp import app
from flask import render_template

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
    # protein: {
    #     'name': 'ajdk',
    #     'description': Loremjkdkjf    
    # }
    return render_template('index.html', title='Kinases', user=user, posts=posts)