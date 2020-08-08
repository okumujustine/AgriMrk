
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# photo upload settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from app.authentication.controllers import authentication
from app.consultation.controllers import consultation
from app.products.controllers import product

app.register_blueprint(authentication, url_prefix='/auth')
app.register_blueprint (consultation, url_prefix='/consultation')
app.register_blueprint (product, url_prefix='/product') 

# create databases
# db.create_all()