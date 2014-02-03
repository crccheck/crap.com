import logging

from dateutil.parser import parse
import requests
from project_runpy import ColorizingStreamHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not len(logger.handlers):
    logger.addHandler(ColorizingStreamHandler())


def _pull(*args):
    url = 'https://spreadsheets.google.com/feeds/{}?alt=json'
    print url.format('/'.join(args))
    return requests.get(url.format('/'.join(args))).json()


def pull(feed, key, worksheet_id=None, visibility='public', projection='values'):
    """
    key:
        worksheets private and public, full and basic
        cells
        list

    worksheet_id:
        should looks like 'od6', 'ocv', etc.

    visibility: private or public
    projection: full basic values
    """
    args = [
        feed,
        key,
    ]
    if worksheet_id:
        args.append(worksheet_id)
    args.append(visibility)
    args.append(projection)
    return _pull(*args)


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


class Spreadsheet(object):
    cells = []
    cols = 0
    rows = 0

    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows
        for row in range(rows):
            self.cells.append(
                [None for __ in range(cols)]
            )

    def import_cell(self, item):
        """Add a cell to the spreadsheet."""
        data = item['gs$cell']
        row = int(data['row']) - 1
        col = int(data['col']) - 1
        # value = data['numericValue'] if 'numericValue' in data else data['$t']
        value = data['$t']
        self.cells[row][col] = value

    def clean(self):
        """Remove excess rows."""
        self.cells = [x for x in self.cells if any(x)]

    @property
    def header(self):
        return self.cells[0]

    @property
    def body(self):
        return self.cells[1:]


def get_worksheet_cells(key, worksheet_id):
    response = pull('cells', key, worksheet_id)
    feed = response['feed']
    cols = int(feed['gs$colCount']['$t'])
    rows = int(feed['gs$rowCount']['$t'])
    spreadsheet = Spreadsheet(rows=rows, cols=cols)
    for cell in feed['entry']:
        spreadsheet.import_cell(cell)
    data = {
        'url': feed['id']['$t'],
        'updated_at': parse(feed['updated']['$t']),
        'title': feed['title']['$t'],
        'author_name': feed['author'][0]['name']['$t'],
        'author_email': feed['author'][0]['email']['$t'],
        'cells': spreadsheet,
    }
    spreadsheet.clean()

    return data
