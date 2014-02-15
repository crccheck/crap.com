from __future__ import print_function
import datetime

from invoke import task


@task(default=True)
def scrape():
    from craptobuy.lib.amazing import lookup_many
    from craptobuy.models import AmazonProduct, PriceHistory

    amazon_batch_limit = 10
    offset = 0

    while True:
        qs = AmazonProduct.select().limit(10).offset(offset)
        offset += amazon_batch_limit  # setup for next iteration

        asin_list = [x.asin for x in qs]
        if not asin_list:
            # exit loop
            break
        lookup = lookup_many(asin_list)
        n_found = 0
        for product in lookup:
            if product.price_and_currency and all(product.price_and_currency):
                PriceHistory.create(
                    asin=product.asin,  # hope this validates
                    price=product.price_and_currency[0],
                    currency=product.price_and_currency[0],
                    retrieved=datetime.datetime.now(),
                )
                n_found += 1
        print('Updated {} out of {} prices'.format(n_found, len(lookup)))
