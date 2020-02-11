import os
from flask import Flask, flash, request, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'webapp/cache/'
ALLOWED_EXTENSIONS = {'tsv'}


application = Flask(__name__)
application.config.from_object(Config)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(application)
migrate = Migrate(application, db)

from webapp import routes, errors, models
