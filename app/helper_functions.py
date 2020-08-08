from flask import request, jsonify
from functools import wraps
from app import app
import jwt

from app.authentication.models import User
from app.helper_variables import (user_admin, user_agronimist, user_customer)

# general helpers
def error_return(status, message):
    return {
        'status': status,
        'message':message
}

def success_return(status, data_object):
    return {
        'status':status,
        'data': data_object
}

# authentication permissions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(error_return(401, "token is missing"))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['user']
        except:
            return jsonify(error_return(401, "token is invalid"))

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(error_return(401, "token is missing"))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['user']
        except:
            return jsonify(error_return(401, "token is invalid"))

        if user_admin not in current_user['roles']:
            print(current_user['roles'])
            return jsonify(error_return(401, "only admin user access"))

        return f(current_user, *args, **kwargs)

    return decorated

def agronomist_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(error_return(401, "token is missing"))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['user']
        except:
            return jsonify(error_return(401, "token is invalid"))

        if any(c_roles in current_user['roles'] for c_roles in (user_admin, user_agronimist)):
            return f(current_user, *args, **kwargs)
        print(current_user['roles'])
        return jsonify(error_return(401, "only admin and agronimoist user access"))

    return decorated

# authentication helpers
def user_exist_by_email(email):
    existing_user_email = User.query.filter_by(email=email).first()
    if existing_user_email:
        return True


def user_exist_by_contact(phone):
    existing_user_contact = User.query.filter_by(phone=phone).first()
    if existing_user_contact:
        return True