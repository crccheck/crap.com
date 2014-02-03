import unittest
from unittest import TestCase

import mock

import gcrap
from gcrap import get_from_url


class GetFromUrlTest(TestCase):
    def test_can_get_key_and_gid(self):
        mock_get_worksheet_meta = mock.MagicMock()
        with mock.patch.multiple(gcrap,
                get_worksheet_meta=mock_get_worksheet_meta):
            get_from_url('http://docs.google.com/spreadsheet/ccc?key=foo&hl=en_US#gid=21')
            mock_get_worksheet_meta.assert_called_with('foo')

        with mock.patch.multiple(gcrap,
                get_worksheet_meta=mock_get_worksheet_meta):
            get_from_url('http://docs.google.com/spreadsheet/ccc?key=bar')
            mock_get_worksheet_meta.assert_called_with('bar')


if __name__ == '__main__':
    unittest.main()
