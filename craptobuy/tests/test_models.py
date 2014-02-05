import datetime
from unittest import TestCase

from ..models import (
    AmazonProduct,
    PriceHistory,
)


class AmazonProductTest(TestCase):
    def test_price_gets_right_value(self):
        asin = AmazonProduct.create(asin='foo')
        PriceHistory.create(asin=asin, price=10, currency='foo',
                retrieved=datetime.datetime.now())
        self.assertEqual(asin.price, 10)

        # assert an even more "current" price is found
        PriceHistory.create(asin=asin, price=11, currency='foo',
                retrieved=datetime.datetime.now() + datetime.timedelta(hours=1))
        self.assertEqual(asin.price, 11)

        # assert an new old price does has no influence
        PriceHistory.create(asin=asin, price=12, currency='foo',
                retrieved=datetime.datetime.now() - datetime.timedelta(hours=1))
        self.assertEqual(asin.price, 11)

    # WISHLIST
    # def test_price_____not_found(self)
