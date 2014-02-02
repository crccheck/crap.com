from flask import (
    render_template,
    redirect,
    url_for,
)

from . import app
from .forms import SubmitEntry
from .models import Comparison
from .utils import parse_url


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
        crap = parse_url(form.data['spreadsheet_url'])
        return redirect(url_for('crap_detail', pk=crap.id))
    # WISHLIST how do I show erros without changing urls?
    return render_template('index.html', form=form)


@app.route('/crap/<int:pk>')
def crap_detail(pk):
    crap = Comparison.get(Comparison.id == pk)
    return render_template('comparison_detail.html', object=crap)
