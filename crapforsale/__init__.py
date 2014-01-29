
from flask import Flask
from playhouse.postgres_ext import PostgresqlExtDatabase


app = Flask(__name__)
app.config.from_object('crapforsale.config')
db = PostgresqlExtDatabase(**app.config['DATABASE'])

from .views import *
