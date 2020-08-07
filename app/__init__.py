
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.authentication.controllers import authentication
from app.consultation.controllers import consultation
from app.products.controllers import product

app.register_blueprint(authentication, url_prefix='/auth')
app.register_blueprint (consultation, url_prefix='/consultation')
app.register_blueprint (product, url_prefix='/product') 

# create databases
db.create_all()