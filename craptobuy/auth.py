# https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
from flask import session, redirect, request, url_for
from flask import jsonify
from flask_oauthlib.client import OAuth

from . import app


oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/account/')
def whoami():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login/')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout/')
def logout():
    session.pop('google_token', None)
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/oauth2callback/')
@google.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    session['user'] = google.get('userinfo').data
    return redirect(url_for('homepage'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
