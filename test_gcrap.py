import unittest
from unittest import TestCase

import mock

import gcrap
from gcrap import get_from_url


class GetFromUrlTest(TestCase):
    def test_can_get_worksheet(self):
        mock_get_worksheet_meta = mock.MagicMock()
        mock_get_worksheet_cells = mock.MagicMock()
        with mock.patch.multiple(gcrap,
            get_worksheet_meta=mock_get_worksheet_meta,
            get_worksheet_cells=mock_get_worksheet_cells,
        ):
            get_from_url('http://docs.google.com/spreadsheet/ccc?key=foo&hl=en_US#gid=21')
            # don't need to call _meta because gid is known
            self.assertFalse(mock_get_worksheet_meta.called)
            mock_get_worksheet_cells.assert_called_with('foo', 'ocv')

    def test_can_guess_worksheet_when_no_gid(self):
        mock_get_worksheet_meta = mock.MagicMock(return_value={
            'worksheets': [{'id': 'baz'}]
        })
        mock_get_worksheet_cells = mock.MagicMock()
        with mock.patch.multiple(gcrap,
            get_worksheet_meta=mock_get_worksheet_meta,
            get_worksheet_cells=mock_get_worksheet_cells,
        ):
            get_from_url('http://docs.google.com/spreadsheet/ccc?key=bar')
            mock_get_worksheet_meta.assert_called_with('bar')
            mock_get_worksheet_cells.assert_called_with('bar', 'baz')


if __name__ == '__main__':
    unittest.main()
