from project_runpy import env


DEBUG = True

CSRF_ENABLED = False
SECRET_KEY = env.get('SECRET')


# DATABASE
SQLALCHEMY_DATABASE_URL = env.get('DATABASE_URL')
