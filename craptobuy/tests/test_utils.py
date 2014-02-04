import random

from unittest import TestCase
import mock

from .. import utils


class ParseUrlTest(TestCase):
    def test_stuff_happens(self):
        n_items = random.randint(5, 10)
        # mock_gsheet = mock.MagicMock()
        # mock_gsheet.return_value = range(n_items)
        # mock_comparison = mock.MagicMock()
        # mock_item = mock.MagicMock()

        # with mock.patch.multiple(utils,
        #         GSpreadsheet=mock_gsheet,
        #         Comparison=mock_comparison,
        #         Item=mock_item):
        #     utils.parse_url('foobar')

        # mock_gsheet.assert_called_once_with('foobar')
        # self.assertEqual(mock_comparison.call_count, 1)
        # self.assertEqual(mock_item.call_count, n_items)


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
