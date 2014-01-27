from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import url, ValidationError


class SubmitEntry(Form):
    spreadsheet_url = URLField(validators=[url()])

    # Custom validators

    def validate_spreadsheet_url(form, field):
        raise ValidationError('test')
