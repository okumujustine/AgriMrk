from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import datetime
import os
import secrets

from app import app, db, photos
from app.helper_functions import (token_required, admin_required, agronomist_required, error_return, success_return)
from app.helper_variables import (ALLOWED_EXTENSIONS)
from app.products.models import Category

# initial product blueprint
product = Blueprint('product', __name__)

@product.route('/')
@agronomist_required
def get_all(current_user):
    return jsonify({"product":"products", "user": current_user})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product.route('/addcategory', methods=['POST', 'GET'])
@admin_required
def add_category():
    category = request.json['category'] 
    if not category:
        return jsonify(error_return(400, 'Empty category field'))

    new_category = Category(name=category)
    db.session.add(new_category)
    db.session.commit()

    return jsonify(success_return(201, {'name':category}))


@product.route('/add', methods=['POST', 'GET'])
def add_product():
    # get form data
    product_form = request.form
    
    # handing files upload
    check_duplicate_imagename = []
    file_one = request.files['imageOne']
    file_two = request.files['imageTwo']
    file_three = request.files['imageThree']
   
    if not file_one.filename or not file_two.filename or not file_three.filename:
        return jsonify(error_return(400, 'Proved all the three(3) images'))

    if not allowed_file(file_one.filename) or not allowed_file(file_two.filename) or not allowed_file(file_three.filename):
        return jsonify(error_return(400, 'Make sure only images are selected among the files'))

    check_duplicate_imagename.extend([file_one.filename, file_two.filename, file_three.filename])
    if len(check_duplicate_imagename) != len(set(check_duplicate_imagename)):
        return jsonify(error_return(400, 'Upload different images or images with different file names'))

    product_image_one = photos.save(file_one, name =  secrets.token_hex(10) + '.')
    product_image_two = photos.save(file_two, name =  secrets.token_hex(10) + '.')
    product_image_three = photos.save(file_three, name =  secrets.token_hex(10) + '.')
    # end of file upload

    # save other informations.
    
    return "new product uploaded"