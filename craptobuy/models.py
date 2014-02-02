from flask import url_for
from peewee import Model, CharField, ForeignKeyField
from playhouse.postgres_ext import JSONField


from . import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = CharField(max_length=120, unique=True)


class Comparison(BaseModel):
    name = CharField(127)
    url = CharField(255, unique=True)
    # user TODO
    # created_at TODO
    # updated_at TODO

    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return url_for('crap_detail', pk=self.id)


class Item(BaseModel):
    data = JSONField()
    comparison = ForeignKeyField(Comparison, related_name='items')
