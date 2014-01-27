from project_runpy import env


DEBUG = True

CSRF_ENABLED = False
SECRET_KEY = env.get('SECRET')
