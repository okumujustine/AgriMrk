from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import os
import secrets

from app import app, db, photos
from app.helper_functions import (token_required, admin_required, agronomist_required, error_return, success_return)
from app.helper_variables import (ALLOWED_EXTENSIONS)
from app.products.models import Category, Product, getProducts, getHireProducts, getProductsFiltered, getCategory
from app.products.schema import products_schema

# initial product blueprint
product = Blueprint('product', __name__)

@product.route('/')
@jwt_required
def get_all(current_user):
    return jsonify({"product":"products", "user": current_user})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product.route('/addcategory', methods=['POST', 'GET'])
@jwt_required
def add_category():
    category = request.json['category'] 
    if not category:
        return jsonify(error_return(400, 'Empty category field'))

    new_category = Category(name=category)
    db.session.add(new_category)
    db.session.commit()

    print(new_category)

    return jsonify(success_return(201, {'name':category}))


@product.route('/add', methods=['POST', 'GET'])
@jwt_required
def add_product():
    # get form data
    product_form = request.form
    title = product_form['title']
    description = product_form['description']
    vendor = product_form['vendor']
    price = product_form['price']
    discount = product_form['discount']
    category = product_form['category']
    stock = product_form['stock']
    sale_type = product_form['saleType']
    category_name = product_form['categoryName']

    # handing files upload
    check_duplicate_imagename = []
    file_one = request.files['imageOne']
    file_two = request.files['imageTwo']
    file_three = request.files['imageThree']
   
    if not file_one.filename or not file_two.filename or not file_three.filename:
        return jsonify(error_return(400, 'Proved all the three(3) images')), 400

    if not allowed_file(file_one.filename) or not allowed_file(file_two.filename) or not allowed_file(file_three.filename):
        return jsonify(error_return(400, 'Make sure only images are selected among the files')), 400

    check_duplicate_imagename.extend([file_one.filename, file_two.filename, file_three.filename])
    if len(check_duplicate_imagename) != len(set(check_duplicate_imagename)):
        return jsonify(error_return(400, 'Upload different images or images with different file names')), 4000

    product_image_one = photos.save(file_one, name =  secrets.token_hex(10) + '.')
    product_image_two = photos.save(file_two, name =  secrets.token_hex(10) + '.')
    product_image_three = photos.save(file_three, name =  secrets.token_hex(10) + '.')
    # end of file upload

    # save other informations.
    try:
        new_product = Product(
            title = title,
            description = description,
            vendor = vendor,
            price = int(price),
            discount = int(discount),
            category_id = category,
            stock = int(stock),
            image_one = product_image_one,
            image_two = product_image_two,
            image_three = product_image_three,
            sale_type = sale_type,
            category_name = category_name
        )
        db.session.add(new_product)
        db.session.commit()
    except:
        return jsonify(error_return(500, 'server failure')), 500
    
    return jsonify(success_return(201, {'data': title}))


@product.route('/hire/get', methods=['GET'])
def get_all_hire_product():
    try:
        page = request.args.get('page', 1, type=int)
        return jsonify(getHireProducts(page)), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 5000


@product.route('/get', methods=['GET', 'POST'])
def get_all_product():
    try:
        page = request.args.get('page', 1, type=int)
        if request.json is not None and bool(request.json["filterObject"]):
            filter_object = request.json["filterObject"]
            return jsonify(getProductsFiltered(page, filter_object)), 200
        
        return jsonify(getProducts(page)), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 5000


@product.route('/category', methods=['GET', 'POST'])
@jwt_required
def get_all_category():
    current_user = get_jwt_identity()
    try:
        return jsonify(getCategory()), 200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000