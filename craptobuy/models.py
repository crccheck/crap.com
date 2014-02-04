import datetime

import amazing
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

    def get_amazon_meta(self):
        # batch query ASINs that were extracted
        almost_items = (self.items.join(AmazonProduct)
                .where(AmazonProduct.title >> None))
        datas = amazing.lookup_many([x.asin.asin for x in almost_items])
        for item, data in zip(almost_items, datas):
            item.store_amazon_meta(data)
        # lookup the rest one by one
        naked_items = self.items.where(Item.asin >> None)
        for item in naked_items:
            item.get_amazon_meta()


class AmazonProduct(BaseModel):
    asin = CharField(max_length=20, primary_key=True)
    active = BooleanField(default=True)
    ##############################
    # fields from the lookup api #
    ##############################
    # http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html
    brand = CharField(255, null=True)
    label = CharField(255, null=True)
    # `large_image_url` 500x500
    image_large = CharField(255, null=True)
    # `medium_image_url` 160x160
    image_medium = CharField(255, null=True)
    # `manufacturer`, `publisher`
    manufacturer = CharField(255, null=True)
    # `model`, `mpn`, `part_number`
    model = CharField(255, null=True)
    # `offer_url`
    url = CharField(255, null=True)
    release_date = DateField(null=True)
    # `title`
    title = CharField(255, null=True)

    #############################
    # Other fields from the API #
    #############################
    # `small_image_url` 75x75
    # `tiny_image_url`
    # `upc`
    # `features`

    def __repr__(self):
        return self.title or self.asin

    #####################
    # CUSTOM PROPERTIES #
    #####################

    @property
    def price(self):
        return (self.asin.pricehistory
            .order_by(PriceHistory.retrieved.desc())
            .first().price
        )


class PriceHistory(BaseModel):
    # `price_and_currency`
    asin = ForeignKeyField(AmazonProduct, related_name='pricehistory')
    price = DecimalField(decimal_places=2)
    currency = CharField(10)
    retrieved = DateTimeField()

    def __repr__(self):
        return u'{} {} {} ({})'.format(
                self.asin, self.price, self.currency, self.retrieved)


class Item(BaseModel):
    """An item in a comparison."""
    data = ArrayField(CharField)
    comparison = ForeignKeyField(Comparison, related_name='items')
    retrieved = DateTimeField()
    asin = ForeignKeyField(AmazonProduct, related_name='items', null=True)

    def __repr__(self):
        return u' '.join(self.data[:2])

    #####################
    # CUSTOM PROPERTIES #
    #####################

    @property
    def price(self):
        return (self.asin.pricehistory
            .order_by(PriceHistory.retrieved.desc())
            .first().price
        )


    ##################
    # CUSTOM METHODS #
    ##################

    def store_amazon_meta(self, product):
        asin = product.asin
        data = dict(
            brand=product.brand,
            label=product.label,
            image_large=product.large_image_url,
            image_medium=product.medium_image_url,
            manufacturer=product.manufacturer,
            model=product.model,
            url=product.offer_url,
            release_date=product.release_date,
            title=product.title,
        )
        try:
            amazonproduct = AmazonProduct.get(asin=asin)
            amazonproduct.update(**data).execute()
        except AmazonProduct.DoesNotExist:
            amazonproduct = AmazonProduct.create(
                    asin=asin, **data)

        if product.price_and_currency and all(product.price_and_currency):
            PriceHistory.create(
                asin=amazonproduct,
                price=product.price_and_currency[0],
                currency=product.price_and_currency[1],
                retrieved=datetime.datetime.now(),
            )

        self.asin = amazonproduct
        self.save()

    def get_amazon_meta(self):
        query = u' '.join(self.data[:2])
        self.store_amazon_meta(amazing.lookup(query))
