from flask import (
    render_template,
    redirect,
    url_for,
)
from gspreadsheet import GSpreadsheet

from . import app
from .forms import SubmitEntry


@app.route('/')
def homepage():
    data = {
        'form': SubmitEntry(),
    }
    return render_template('index.html', **data)


@app.route('/done/')
def crap():
    return 'Crap'


@app.route('/add/', methods=('POST', ))
def add_crap():
    form = SubmitEntry()
    if form.validate_on_submit():
        sheet = GSpreadsheet(form.data['spreadsheet_url'])
        # TODO save new Sheet object
        for row in sheet:
            # TODO save new Row object
            pass
        return redirect(url_for('crap'))
    # WISHLIST how do I show erros without changing urls?
    return render_template('index.html', form=form)
