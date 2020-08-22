from flask import Blueprint, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import jwt
import json


from app import db, app
from app.authentication.models import User, Role
from app.authentication.schema import user_schema
from app.helper_functions import (
    error_return,
    success_return,
    user_exist_by_email,
    user_exist_by_contact
)
from app.helper_functions import token_required

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
    role = new_user['role']

    if user_exist_by_contact(phone):
        return jsonify(error_return(400, 'user with phone already exists'))

    if user_exist_by_email(email):
        return jsonify(error_return(400, 'user with email address already exists'))

    hashed_password = generate_password_hash(password)

    new_user_data = User(country, region, district, phone, name, email, hashed_password, status)
    new_user_role = Role.query.filter_by(role=role).first()
    if not new_user_role:
        return jsonify(error_return(404, 'user role does not exist'))

    new_user_data.roles.append(new_user_role)
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
  
    if len(phone.strip())==0 or len(password.strip())==0:
        return jsonify(error_return(400, 'all required fields must be provided.')), 400

    if not phone.isdigit():
        return jsonify(error_return(400, 'invalid phone number.')), 400

    existing_user = User.query.filter_by(phone=phone).first()
    existing_user_roles = []

    if not existing_user:
        return jsonify(error_return(404, 'user does not exists')), 404

    if not check_password_hash(existing_user.password, password):
        return jsonify(error_return(400, 'incorrect contact or password')), 404

    for roles in existing_user.roles:
        existing_user_roles.append(roles.role)

    logged_in_user = {
        'id':existing_user.id,
        'country':existing_user.country,
        'region':existing_user.region,
        'district':existing_user.district,
        'phone':existing_user.phone,
        'name':existing_user.name,
        'email':existing_user.email,
        'status':existing_user.status,
        'roles': existing_user_roles
    }     

    token = jwt.encode({
        'user':logged_in_user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=2)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify(success_return(200, {'token':token.decode('utf-8'), 'user':logged_in_user} ))
    # return user_schema.jsonify(existing_user)



@authentication.route('/user', methods =['GET'])
@token_required
def current_logged_in_user(current_user):
    return jsonify({'current_user':current_user})

