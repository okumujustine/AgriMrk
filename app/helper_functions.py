from flask import request, jsonify
from functools import wraps
from app import app
import jwt

from app.authentication.models import User

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

# authentication helpers
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify(error_return(401, "token is missing"))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify(error_return(401, "token is invalid"))
        return f(*args, **kwargs)

    return decorated

def user_exist_by_email(email):
    existing_user_email = User.query.filter_by(email=email).first()
    if existing_user_email:
        return True


def user_exist_by_contact(phone):
    existing_user_contact = User.query.filter_by(phone=phone).first()
    if existing_user_contact:
        return True