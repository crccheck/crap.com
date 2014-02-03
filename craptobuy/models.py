from flask import url_for
from peewee import Model, CharField, ForeignKeyField
from playhouse.postgres_ext import ArrayField


from . import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(max_length=100)
    email = CharField(max_length=120, unique=True)

    def __repr__(self):
        return u'{} <{}>'.format(self.name, self.email)


class Comparison(BaseModel):
    name = CharField(127)
    url = CharField(255, unique=True)
    header = ArrayField(CharField)
    user = ForeignKeyField(User, null=True)
    # created_at
    # updated_at

    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return url_for('crap_detail', pk=self.id)

    #####################
    # CUSTOM PROPERTIES #
    #####################

    @property
    def columns(self):
        return self.items.first().data.keys()


class Item(BaseModel):
    data = ArrayField(CharField)
    comparison = ForeignKeyField(Comparison, related_name='items')

    def __repr__(self):
        return u' '.join(self.data[:2])
