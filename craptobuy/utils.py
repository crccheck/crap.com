from gspreadsheet import GSpreadsheet

from .models import Comparison, Item


def parse_url(url):
    sheet = GSpreadsheet(url)

    try:
        comparison = Comparison.get(url=url)
        Item.delete().where(Item.comparison == comparison)
    except Comparison.DoesNotExist:
        comparison = Comparison.create(
            url=url,
            name=sheet.feed.title.text,
        )
    for row in sheet:
        data = row.copy()  # to get this JSON serializable
        Item.create(comparison=comparison, data=data)

    return comparison
