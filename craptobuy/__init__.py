
from flask import Flask
from playhouse.postgres_ext import PostgresqlExtDatabase


app = Flask(__name__)
app.config.from_object('craptobuy.config')
db = PostgresqlExtDatabase(
        # let me be lazier
        autocommit=True,
        autorollback=True,
        **app.config['DATABASE'])

from .views import *
