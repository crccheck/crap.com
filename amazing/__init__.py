from amazon.api import AmazonAPI
from project_runpy import env


AMAZON_ASSOC_TAG = env.get('AMAZON_ASSOC_TAG')
AMAZON_SECRET_KEY = env.get('AMAZON_SECRET_KEY')
AMAZON_ACCESS_KEY = env.get('AMAZON_ACCESS_KEY')


def get_api():
    return AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)


def lookup(query):
    """
    Find a product on amazon.

    SearchIndex are: 'All', 'Apparel', 'Appliances', 'ArtsAndCrafts',
    'Automotive', 'Baby', 'Beauty', 'Blended', 'Books', 'Classical',
    'Collectibles', 'DVD', 'DigitalM usic', 'Electronics', 'GiftCards',
    'GourmetFood', 'Grocery', 'HealthPersonalCare', 'HomeGarden', 'Industrial',
    'Jewelry', 'KindleStore', 'Kitchen', 'LawnAndGarde n', 'Marketplace',
    'MP3Downloads', 'Magazines', 'Miscellaneous', 'Music', 'MusicTracks',
    'MusicalInstruments', 'MobileApps', 'OfficeProducts', 'OutdoorLiving',
    'PCHardware', 'PetSupplies', 'Photo', 'Shoes', 'Software', 'SportingGoods',
    'Tools', 'Toys', 'UnboxVideo', 'VHS', 'Video', 'VideoGames', 'Watches',
    'Wireless', 'WirelessAccessories'

    Keywords that can be used:
    http://docs.aws.amazon.com/AWSECommerceService/latest/DG/USSearchIndexParamForItemsearch.html
    """
    amazon = get_api()
    products = amazon.search_n(1, Keywords=query, SearchIndex='All')
    return products[0]
