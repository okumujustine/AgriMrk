
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, send

app = Flask(__name__, static_folder='../static')

app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
JWTManager(app)

# socketio init
socketio = SocketIO(app, cors_allowed_origins="*")

# photo upload settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from app.authentication.controllers import authentication
from app.consultation.controllers import consultation
from app.products.controllers import product
from app.orders.controllers import orders
from app.blog.controllers import blog

app.register_blueprint(authentication, url_prefix='/auth')
app.register_blueprint (consultation, url_prefix='/consultation')
app.register_blueprint (product, url_prefix='/product') 
app.register_blueprint(orders, url_prefix='/orders')
app.register_blueprint(blog, url_prefix='/blog')

# create databases
# db.create_all()