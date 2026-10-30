import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)
# Damit wird die Flask-App mit dem Flask-SQLAlchemy-Code verbunden.
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', title='Home', user='Alice')



