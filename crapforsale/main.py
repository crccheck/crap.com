from flask import Flask, render_template
from project_runpy import env


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    if env.get('DEBUG'):
        app.debug = True
    app.run(host='0.0.0.0')
