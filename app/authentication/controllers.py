from flask import Blueprint

from app.authentication.models import User

authentication = Blueprint('authentication', __name__)

@authentication.route('/')
def index():
    return "we are home boys"