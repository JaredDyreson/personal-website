from __future__ import absolute_import
from flask import Flask
import pathlib


UPLOAD_FOLDER = pathlib.Path('/home/jared/storage')

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from personalwebsite import routes
