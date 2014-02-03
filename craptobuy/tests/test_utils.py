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
