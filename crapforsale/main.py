from flask import (
    Flask, render_template,
    redirect,
)

from forms import SubmitEntry

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def homepage():
    data = {
        'form': SubmitEntry(),
    }
    return render_template('index.html', **data)


@app.route('/add/', methods=('POST', ))
def addCrap():
    form = SubmitEntry()
    if form.validate_on_submit():
        pass
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
