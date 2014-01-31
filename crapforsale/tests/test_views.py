import unittest

from flask import url_for
import mock

from ..views import app, add_crap


class TestAddCrap(unittest.TestCase):
    def setUp(self):
        self.view = add_crap
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_it_tries_to_get_a_spreadsheet(self):
        form_data = {'spreadsheet_url': 'http://example.com/key=ff'}
        url = url_for('add_crap')

        with mock.patch('crapforsale.views.GSpreadsheet') as g:
            c = app.test_client()
            response = c.post(url, data=form_data)
            self.assertEqual(response.status_code, 302)
            g.assert_called_once_with(form_data['spreadsheet_url'])
