
from flask import Flask
from peewee import PostgresqlDatabase


app = Flask(__name__)
app.config.from_object('crapforsale.config')
db = PostgresqlDatabase(**app.config['DATABASE'])

from .views import *
