from unittest import TestCase
import mock

from .. import models
from .. import utils


class DatahashTest(TestCase):
    """datahash()"""
    def test_it_runs(self):
        row = ['a', 'b', 'c']
        self.assertTrue(utils.datahash(row))

    def test_update_concatenate_same_diff(self):
        row = ['a', 'b', 'c']
        h1 = utils.datahash(row)
        self.assertEqual(utils.datahash(['abc']), h1)
        self.assertEqual(utils.datahash(['a', 'bc']), h1)
        self.assertEqual(utils.datahash(['ab', 'c']), h1)


class ParseSheetTest(TestCase):
    """parse_sheet()"""

    def setUp(self):
        mock_sheet = {}
        mock_sheet['key'] = 'foobar'
        mock_sheet['worksheet_id'] = 'od6'
        mock_sheet['author_email'] = 'dummy@example.com'
        mock_sheet['title'] = 'sheet title'
        mock_data = mock.MagicMock()
        mock_sheet['cells'] = mock_data
        mock_data.header = ['h1', 'h2']
        mock_data.body = []
        self.sheet = mock_sheet
        self.data = mock_data

    def tearDown(self):
        # clear all comparisons and items
        for c in models.Comparison.select():
            c.delete_instance(recursive=True)


    def test_comparison_is_created(self):
        comparison = utils.parse_sheet(self.sheet, 'http://foobar')

        # assert comparison was made
        self.assertTrue(comparison)
        # assert comparison is in the database
        self.assertTrue(comparison.id)

    def test_rows_are_saved(self):
        # test setup
        self.data.body = [
            ['1'],
            ['2'],
            ['3'],
            ['4'],
        ]

        comparison = utils.parse_sheet(self.sheet, 'http://foobar')
        self.assertEqual(comparison.items.count(), 4)

    def test_repeated_runs_clear_old_rows(self):
        self.data.body = [
            ['1'],
            ['2'],
            ['3'],
            ['4'],
        ]
        comparison = utils.parse_sheet(self.sheet, 'http://foobar')

        self.data.body = [
            ['5'],
            ['6'],
        ]
        comparison = utils.parse_sheet(self.sheet, 'http://foobar')

        self.assertEqual(comparison.items.count(), 2)


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
