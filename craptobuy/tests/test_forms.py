# from flask.ext.testing import TestCase
from unittest import TestCase
import mock
from wtforms.validators import ValidationError

from ..forms import SubmitEntry


class SubmitEntryTest(TestCase):
    def test_validate_spreadsheet_url(self):
        form = SubmitEntry.__new__(SubmitEntry)
        valid_data = (
            'https://docs.google.com/spreadsheet/ccc?'
                    'key=0AvtWFMTdBQSLdFI3Y2M0RnI5OTBMa2FydXNFelBDTUE',
        )
        invalid_data = (
            '',
            'http://example.com',
            # TODO
        )

        mock_field = mock.MagicMock()

        # does not raise error
        for data in valid_data:
            mock_field.data = data
            form.validate_spreadsheet_url(mock_field)

        for data in invalid_data:
            mock_field.data = data
            with self.assertRaises(ValidationError):
                form.validate_spreadsheet_url(mock_field)
