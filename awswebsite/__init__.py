from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = sql(app)

from awswebsite import routes

