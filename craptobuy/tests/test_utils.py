from unittest import TestCase
import mock

from .. import utils


class ParseSheetTest(TestCase):
    """parse_sheet()"""
    def test_stuff_happens(self):
        # setup
        mock_sheet = {}
        mock_sheet['key'] = 'foobar'
        mock_sheet['worksheet_id'] = 'od6'
        mock_sheet['author_email'] = 'dummy@example.com'
        mock_sheet['title'] = 'sheet title'
        mock_data = mock.MagicMock()
        mock_sheet['cells'] = mock_data
        mock_data.header = ['h1', 'h2']
        mock_data.body = []

        comparison = utils.parse_sheet(mock_sheet, 'http://foobar')

        # assert comparison was made
        self.assertTrue(comparison)
        # assert comparison is in the database
        self.assertTrue(comparison.id)



class FindASINTest(TestCase):
    def test_it_works(self):
        B00032G1S0 = 'http://www.amazon.com/Tuscan-Whole-Milk-Gallon-128/dp/B00032G1S0/ref=sr_1_1?ie=UTF8&qid=1391488553&sr=8-1&keywords=milk+gallon'

        row = []
        result = utils.find_asin(row)
        self.assertIsNone(result)

        row = [None]
        result = utils.find_asin(row)
        self.assertIsNone(result)

        row = ['http://www.amazon.com/']
        result = utils.find_asin(row)
        self.assertIsNone(result)

        row = [
            B00032G1S0,
        ]
        result = utils.find_asin(row)
        self.assertEqual(result, 'B00032G1S0')
