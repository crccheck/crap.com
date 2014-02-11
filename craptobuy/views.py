from flask import (
    render_template,
    redirect,
    url_for,
)

from . import app
from .forms import SubmitEntry
from .models import Comparison, Item, AmazonProduct
from .utils import parse_url


@app.route('/')
def homepage():
    data = {
        'form': SubmitEntry(),
        'recent_craps':
            Comparison.select().order_by(Comparison.modified.desc()).limit(10)
    }
    return render_template('index.html', **data)


@app.route('/crap/')
def crap():
    return redirect(url_for('crap_list'))


@app.route('/craps/')
def crap_list():
    craps = Comparison.select()
    return render_template('comparison_list.html', object_list=craps)


@app.route('/add/', methods=('POST', ))
def add_crap():
    form = SubmitEntry()
    if form.validate_on_submit():
        crap = parse_url(form.data['spreadsheet_url'])
        return redirect(url_for('crap_detail', pk=crap.id))
    # WISHLIST how do I show erros without changing urls?
    return render_template('index.html', form=form)


@app.route('/crap/<int:pk>/')
def crap_detail(pk):
    crap = Comparison.get(Comparison.id == pk)
    return render_template('comparison_detail.html', object=crap)


@app.route('/crap/<int:pk>/refresh/', methods=('POST', ))
def crap_refresh(pk):
    """Manually refresh spreadsheet."""
    crap = Comparison.get(Comparison.id == pk)
    crap.refresh()
    return redirect(url_for('crap_detail', pk=crap.id))


@app.route('/crap/<int:pk>/price/', methods=('POST', ))
def crap_price(pk):
    """Manually pull prices and thumbnail."""
    crap = Comparison.get(Comparison.id == pk)
    crap.get_amazon_meta()
    return redirect(url_for('crap_detail', pk=crap.id))


@app.route('/items/')
def item_list():
    queryset = Item.select()
    return render_template('item_list.html', object_list=queryset)


@app.route('/asins/')
def asin_list():
    queryset = AmazonProduct.select()
    return render_template('item_list.html', object_list=queryset)
