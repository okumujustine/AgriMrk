
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FLASK_ENV = 'development'
# FLASK_ENV = 'production'


if FLASK_ENV == 'development':
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
else:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
THREADS_PER_PAGE = 2

# Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
