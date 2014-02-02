from gspreadsheet import GSpreadsheet

from .models import Comparison, Item


def parse_url(url):
    sheet = GSpreadsheet(url)

    comparison = Comparison.create(url=url, name=url)
    for row in sheet:
        data = row.copy()  # to get this JSON serializable
        Item.create(comparison=comparison, data=data)

    return comparison.id
