import datetime
import re
from hashlib import md5

from .lib.gcrap import get_from_url

from .models import Comparison, AmazonProduct, Item


ASIN_PATTERN = re.compile(r'http.*amazon.com.*/dp/(\w+)/',flags=re.IGNORECASE)


def parse_url(url):
    sheet = get_from_url(url)
    return parse_sheet(sheet, url=url)


def datahash(row):
    """Get a hash for a row of data."""
    m = md5()
    for x in row:
        m.update(x)
    return m.hexdigest()[:8]


def parse_sheet(sheet, url=None):
    import_start = datetime.datetime.now()
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
            author_email=sheet['author_email'],
            name=sheet['title'],
            header=sheet['cells'].header,
            modified=import_start,
        )
    for row in sheet['cells'].body:
        asin = find_asin(row)
        if asin:
            product = AmazonProduct.get_or_create(asin=asin)
        else:
            product = None
        Item.create(comparison=comparison, data=row,
                asin=product,
                retrieved=import_start)

    return comparison


def find_asin(row):
    """Look for an Amazon ASIN in a row of data."""
    for col in row:
        if not col:
            continue
        found = ASIN_PATTERN.match(col)
        if found:
            return found.group(1)
