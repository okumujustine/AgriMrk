
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FLASK_ENV = 'development'
# FLASK_ENV = 'production'


if FLASK_ENV == 'development':
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/ag'
else:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://lbbfootqtsnkxa:a5e884b30556d3dd738a5fcfc6be698813a12761417ad0e02f93869fe5fc046c@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d4l49r60802obs'

DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
THREADS_PER_PAGE = 2

# Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
