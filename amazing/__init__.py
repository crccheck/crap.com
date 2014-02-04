from amazon.api import AmazonAPI
from project_runpy import env


AMAZON_ASSOC_TAG = env.get('AMAZON_ASSOC_TAG')
AMAZON_SECRET_KEY = env.get('AMAZON_SECRET_KEY')
AMAZON_ACCESS_KEY = env.get('AMAZON_ACCESS_KEY')

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
