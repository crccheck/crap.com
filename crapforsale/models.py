from peewee import Model, CharField

from . import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = CharField(max_length=120, unique=True)


class Spreadsheet(BaseModel):
    name = CharField(127)
    url = CharField(255, unique=True)
    # user TODO
    # created_at TODO
    # updated_at TODO


class Row(BaseModel):
    pass
    # data = db.Column(JSON) TODO
