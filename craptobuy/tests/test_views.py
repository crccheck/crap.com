from unittest import TestCase

from flask import url_for
import mock

from ..views import app, add_crap


class TestAddCrap(TestCase):
    def setUp(self):
        self.view = add_crap
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_it_tries_to_get_a_spreadsheet(self):
        form_data = {'spreadsheet_url': 'https://docs.google.com/spreadsheet/'
                'ccc?key=0AvtWFMTdBQSLdFI3Y2M0RnI5OTBMa2FydXNFelBDTUE'}
        url = url_for('add_crap')

        with mock.patch('craptobuy.views.parse_url') as g:
            c = app.test_client()
            response = c.post(url, data=form_data)
            self.assertEqual(response.status_code, 302)
            g.assert_called_once_with(form_data['spreadsheet_url'])
