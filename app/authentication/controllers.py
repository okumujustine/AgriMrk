from flask import Blueprint, request
from app import db
from app.authentication.models import User

authentication = Blueprint('authentication', __name__)

@authentication.route('/')
def index():
    return "we are home boys"


@authentication.route('/signup', methods =['GET', 'POST'])
def signup():
    new_user = request.json
    country = new_user['country']
    name = new_user['name']
    region = new_user['region']
    district = new_user['district']
    phone = new_user['phone']
    email = new_user['email']
    password = new_user['password']
    status = new_user['status']
    
    new_user_data = User(country, region, district, phone, name, email, password, status)
    db.session.add(new_user_data)
    db.session.commit()

    return "signup here"