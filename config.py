
import os
from flask_uploads import IMAGES

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FLASK_ENV = 'development'
# FLASK_ENV = 'production'


if FLASK_ENV == 'development':
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/agrimrk'
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
SECRET_KEY = "agriculturefordevelopement"

JWT_SECRET_KEY = "myawesomesecretisnevergonnagiveyouup"

# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/image/uploads')
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024

UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/image/uploads')
