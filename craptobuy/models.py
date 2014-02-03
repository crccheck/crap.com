import datetime

from flask import url_for
from gcrap import get_worksheet_cells
from peewee import Model, CharField, DateTimeField, ForeignKeyField
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
    key = CharField(70)  # key
    worksheet_id = CharField(4)  # worksheet id
    url = CharField(255)  # the url the user submitted
    header = ArrayField(CharField)
    user = ForeignKeyField(User, null=True, related_name='comparisons')
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField()

    class Meta:
        indexes = (
            (('key', 'worksheet_id'), True),
        )

    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return url_for('crap_detail', pk=self.id)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        return super(Comparison, self).save(*args, **kwargs)

    #####################
    # CUSTOM PROPERTIES #
    #####################

    @property
    def columns(self):
        return self.items.first().data.keys()

    ##################
    # CUSTOM METHODS #
    ##################

    def refresh(self):
        """Re-pull data from the Google."""
        qs = Item.delete().where(Item.comparison == self)
        qs.execute()
        sheet = get_worksheet_cells(self.key, self.worksheet_id)
        for row in sheet['cells'].body:
            Item.create(comparison=self, data=row)


class Item(BaseModel):
    data = ArrayField(CharField)
    comparison = ForeignKeyField(Comparison, related_name='items')

    def __repr__(self):
        return u' '.join(self.data[:2])
