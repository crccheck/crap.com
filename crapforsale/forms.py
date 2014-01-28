import re

from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import url, ValidationError


class SubmitEntry(Form):

    # Custom validators

    def validate_spreadsheet_url(form, field):
        # TODO make sure url is a Google Spreadsheets url to avoid slow external
        # check.
        if not re.search(r'key', field.data):
            raise ValidationError('Not a Google Spreadsheet URL')

    spreadsheet_url = URLField(validators=[
            url(), validate_spreadsheet_url])
