from flask import Blueprint, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,create_refresh_token, jwt_refresh_token_required
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
        return jsonify(error_return(400, 'user with phone already exists')), 400

    if user_exist_by_email(email):
        return jsonify(error_return(400, 'user with email address already exists')), 400
    
    hashed_password = generate_password_hash(password)

    new_user_data = User(country, region, district, phone, name, email, hashed_password, status)
    new_user_role = Role.query.filter_by(role=role).first()
    if not new_user_role:
        return jsonify(error_return(404, 'user role does not exist')), 404

    new_user_data.roles.append(new_user_role)
    db.session.add(new_user_data)
    db.session.commit()

    return jsonify(success_return(201, {
        'name':name,
        'phone':phone
    })), 201



@authentication.route('/login', methods =['GET', 'POST'])
def login():
    user = request.json
    phone = user['phone']
    password = user['password']
  
    if not phone or len(password.strip())==0:
        return jsonify(error_return(400, 'all required fields must be provided.')), 400

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

    expires = datetime.timedelta(seconds=10)
    token = create_access_token(identity=logged_in_user, expires_delta=expires)
    refresh_token = create_refresh_token(identity=logged_in_user)

    return jsonify(success_return(200, {'token':token, "refreshToken": refresh_token, 'user':logged_in_user} )), 200


@authentication.route('/user', methods =['GET'])
@jwt_required
def current_logged_in_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200


@authentication.route("/checkiftokenexpire", methods=["POST"])
@jwt_required
def check_if_token_expire():
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify({"success": True})


@authentication.route("/refreshtoken", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    expires = datetime.timedelta(seconds=10)
    token = create_access_token(identity=identity, expires_delta=expires)
    return jsonify({"token": token})

