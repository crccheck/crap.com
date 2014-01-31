from gspreadsheet import GSpreadsheet

from .models import Comparison, Item


def parse_url(url):
    sheet = GSpreadsheet(url)

    comparison = Comparison(url=url)
    for row in sheet:
        Item(comparison=comparison, data=row)
