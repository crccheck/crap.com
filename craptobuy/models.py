import datetime

from flask import url_for
from gcrap import get_worksheet_cells
from peewee import (
    Model,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKeyField,
)
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


class AmazonProduct(BaseModel):
    asin = CharField(max_length=20, primary_key=True)
    active = BooleanField(default=True)
    ##############################
    # fields from the lookup api #
    ##############################
    # http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html
    brand = CharField(255)
    label = CharField(255)
    # `large_image_url` 500x500
    image_large = CharField(255)
    # `medium_image_url` 160x160
    image_medium = CharField(255)
    # `manufacturer`, `publisher`
    manufacturer = CharField(255)
    # `model`, `mpn`, `part_number`
    model = CharField(255)
    # `offer_url`
    url = CharField(255)
    release_date = DateField()
    # `title`
    title = CharField(255)

    #############################
    # Other fields from the API #
    #############################
    # `small_image_url` 75x75
    # `tiny_image_url`
    # `upc`
    # `features`

    def __repr__(self):
        return self.title


class PriceHistory(BaseModel):
    # `price_and_currency`
    asin = ForeignKeyField(AmazonProduct, related_name='pricehistory')
    price = DecimalField(decimal_places=2)
    currency = CharField(10)
    retrieved = DateTimeField()

    def __repr__(self):
        return u'{} {}'.format(self.asin, self.retrieved)


class Item(BaseModel):
    """An item in a comparison."""
    data = ArrayField(CharField)
    comparison = ForeignKeyField(Comparison, related_name='items')
    retrieved = DateTimeField()
    asin = ForeignKeyField(AmazonProduct, related_name='items', null=True)

    def __repr__(self):
        return u' '.join(self.data[:2])
