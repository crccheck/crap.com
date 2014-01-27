from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import url


class SubmitEntry(Form):
    spreadsheet_url = URLField(validators=[url()])
