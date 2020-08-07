from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import jwt


from app import db, app
from app.authentication.models import User
from app.authentication.schema import user_schema
from app.helper_functions import (
    error_return,
    success_return,
    user_exist_by_email,
    user_exist_by_contact
)

# initialization blueprint
authentication = Blueprint('authentication', __name__)


@authentication.route('/signup', methods =['GET', 'POST'])
def signup():
    new_user = request.json
    phone = new_user['phone']
    email = new_user['email']
    country = new_user['country']
    name = new_user['name']
    region = new_user['region']
    district = new_user['district']
    password = new_user['password']
    status = new_user['status']

    if user_exist_by_contact(phone):
        return jsonify(error_return(301, 'user with phone already exists'))

    if user_exist_by_email(email):
        return jsonify(error_return(301, 'user with email address already exists'))

    hashed_password = generate_password_hash(password)

    new_user_data = User(country, region, district, phone, name, email, hashed_password, status)
    db.session.add(new_user_data)
    db.session.commit()

    return jsonify(success_return(201, {
        'name':name,
        'phone':phone
    }))



@authentication.route('/login', methods =['GET', 'POST'])
def login():
    user = request.json
    phone = user['phone']
    password = user['password']

    existing_user = User.query.filter_by(phone=phone).first()

    if not existing_user:
        return jsonify(error_return(404, 'user does not exists'))

    if not check_password_hash(existing_user.password, password):
        return jsonify(error_return(400, 'incorrect contact or password'))

    logged_in_user = {
        'country':existing_user.country,
        'region':existing_user.region,
        'district':existing_user.district,
        'phone':existing_user.phone,
        'name':existing_user.name,
        'email':existing_user.email,
        'status':existing_user.status
    }     

    token = jwt.encode({
        'user':logged_in_user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=4)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify(success_return(200, {'token':token.decode('utf-8')} ))

