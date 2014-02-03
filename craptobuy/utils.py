from gcrap import get_from_url

from .models import Comparison, Item


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
            header=sheet['cells'].header
        )
    for row in sheet['cells'].body:
        Item.create(comparison=comparison, data=row)

    return comparison
