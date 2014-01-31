import urlparse

from project_runpy import env


DEBUG = True

SECRET_KEY = env.get('SECRET_KEY')


# DATABASE
urlparse.uses_netloc.append('postgresql')
url = urlparse.urlparse(env.get('DATABASE_URL'))
DATABASE = {
    'database': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port,
}