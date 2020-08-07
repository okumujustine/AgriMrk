from flask import Blueprint, jsonify
from app.helper_functions import (token_required)

# initial product blueprint
product = Blueprint('product', __name__)

@product.route('/')
@token_required
def get_all(current_user):
    return jsonify({"product":"products", "user": current_user})