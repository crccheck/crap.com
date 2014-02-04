import datetime
import re

from gcrap import get_from_url

from .models import Comparison, AmazonProduct, Item


asin_pattern = re.compile(r'http.*amazon.com.*/dp/(\w+)/',flags=re.IGNORECASE)
def parse_url(url):
    sheet = get_from_url(url)

    try:
        comparison = Comparison.get(
            key=sheet['key'],
            worksheet_id=sheet['worksheet_id'],
        )
        qs = Item.delete().where(Item.comparison == comparison)
        qs.execute()
    except Comparison.DoesNotExist:
        comparison = Comparison.create(
            key=sheet['key'],
            worksheet_id=sheet['worksheet_id'],
            url=url,
            name=sheet['title'],
            header=sheet['cells'].header,
            modified=datetime.datetime.now(),
        )
    for row in sheet['cells'].body:
        asin = find_asin(row)
        if asin:
            product = AmazonProduct.get_or_create(asin=asin)
        else:
            product = None
        Item.create(comparison=comparison, data=row,
                asin=product,
                retrieved=datetime.datetime.now())

    return comparison


def find_asin(row):
    """Look for an Amazon ASIN in a row of data."""
    for col in row:
        if not col:
            continue
        found = asin_pattern.match(col)
        if found:
            return found.group(1)
