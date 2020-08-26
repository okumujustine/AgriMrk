
from flask import Blueprint, request, jsonify, Response
import secrets
from app import db

from app.orders.models import CustomerOder
from app.orders.schema import orders_schema
from app.helper_functions import token_required, success_return, error_return

orders = Blueprint('orders', __name__)

@orders.route('/')
def get_all():
    get_orders = CustomerOder.query.all()
    print(get_orders)
    
    return orders_schema.jsonify(get_orders)


@orders.route('/add', methods=['POST', 'GET'])
@token_required
def add_orders(current_user):
    if request.method == 'POST':
        cart_items = request.json['order'] 
        invoice_number = secrets.token_hex(5)
        if not cart_items:
            return jsonify(error_return(400, 'No order items')), 400
        print(cart_items)
        try:
            final_order = CustomerOder(
                invoice=invoice_number,
                status="pending",
                address=current_user["district"],
                phone=current_user["phone"],
                customer_id=current_user["id"],
                orders=cart_items
            )
            db.session.add(final_order)
            db.session.commit()
        except:
            return jsonify(error_return(500, 'Server failure, try again later!')), 500

        return jsonify(success_return(200,{"success":"Order created", "user":current_user})), 200
    else:
        return jsonify({"failed":"invalid request"})