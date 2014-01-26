from flask import Flask
from project_runpy import env


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    if env.get('DEBUG'):
        app.debug = True
    app.run(host='0.0.0.0')
