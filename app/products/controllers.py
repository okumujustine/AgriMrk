from flask import Blueprint, jsonify
from app.helper_functions import (token_required, admin_required, agronomist_required)

# initial product blueprint
product = Blueprint('product', __name__)

@product.route('/')
@agronomist_required
def get_all(current_user):
    return jsonify({"product":"products", "user": current_user})