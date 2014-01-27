from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)
from flask.ext.sqlalchemy import SQLAlchemy


from forms import SubmitEntry

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

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
def addCrap():
    form = SubmitEntry()
    if form.validate_on_submit():
        return redirect(url_for('crap'))
    # TODO how do I show erros without changing urls?
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
