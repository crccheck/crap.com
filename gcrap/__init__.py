import logging

from dateutil.parser import parse
import requests
from project_runpy import ColorizingStreamHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not len(logger.handlers):
    logger.addHandler(ColorizingStreamHandler())


def _pull(**kwargs):
    url = 'https://spreadsheets.google.com/feeds/{feed}/{key}/{visibility}/{projection}?alt=json'
    return requests.get(url.format(**kwargs)).json()


def pull(feed, key, visibility='public', projection='values'):
    """
    key:
        worksheets private and public, full and basic

    visibility: private or public
    projection: full basic values
    """
    kwargs = dict(
        feed=feed,
        key=key,
        visibility=visibility,
        projection=projection,
    )
    return _pull(**kwargs)


def get_worksheet_meta(key):
    response = pull('worksheets', key)
    feed = response['feed']
    worksheets = []
    for item in feed['entry']:
        worksheet_id = item['id']['$t'].rsplit('/', 1)[1]
        worksheets.append({
            'id': worksheet_id,
            'updated_at': parse(item['updated']['$t']),
            'title': item['title']['$t'],
        })
    data = {
        'url': feed['id']['$t'],
        'updated_at': parse(feed['updated']['$t']),
        'title': feed['title']['$t'],
        'author_name': feed['author'][0]['name']['$t'],
        'author_email': feed['author'][0]['email']['$t'],
        'worksheets': worksheets,
    }
    return data
