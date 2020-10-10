
from flask import Blueprint, request, jsonify, Response
from rave_python import Rave, RaveExceptions, Misc
from flask_jwt_extended import jwt_required, get_jwt_identity
import secrets
from app import db

from app.orders.models import CustomerOder, CustomerHireOder, getHireOrdersList, getHireOrdersListFiltered
from app.orders.schema import orders_schema, hire_products_schema
from app.helper_functions import token_required, success_return, error_return

orders = Blueprint('orders', __name__)

@orders.route('/')
def get_all():
    get_orders = CustomerOder.query.all()
    print(get_orders)
    
    return orders_schema.jsonify(get_orders)


@orders.route('/add', methods=['POST', 'GET'])
@jwt_required
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


# CustomerHireOder -> get hire orders
@orders.route('/hirelist', methods=['POST','GET'])
@jwt_required
def get_hire_orders_list():
    current_user = get_jwt_identity()
    customer_id = current_user["id"]
    print(request.json)
    try:
        page = request.args.get('page', 1, type=int)
        if request.json is not None and bool(request.json["filterObject"]):
            filter_object = request.json["filterObject"]
            return jsonify(getHireOrdersListFiltered(page, customer_id, filter_object)), 200
        
        return jsonify(getHireOrdersList(page, customer_id)), 200
        
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 5000


# CustomerHireOder -> add hire order
@orders.route('/hire/add', methods=['POST', 'GET'])
@jwt_required
def add_hire_orders():
    if request.method == 'POST':
        #  TODO : create validations here
        current_user = get_jwt_identity()
        invoice_hire_number = secrets.token_hex(5)
        address = request.json["address"]
        phone = request.json["phone"]
        hire_notes = request.json["hireNote"]
        needed_date = request.json["neededDate"]
        return_date = request.json["returnDate"]
        days_number = request.json["days"]
        product_name = request.json["productName"]
        product_id = request.json["productId"]
        customer_id = current_user["id"]
        
        try:
            final_hire_order = CustomerHireOder(
                hire_number = invoice_hire_number,
                status = "pending",
                address = address,
                phone = phone,
                hire_notes = hire_notes,
                needed_date = needed_date,
                return_date = return_date,
                days_number = int(days_number),
                product_name = product_name,
                product_id = product_id,
                customer_id = customer_id
            )
            db.session.add(final_hire_order)
            db.session.commit()
            return jsonify(success_return(200,{"success":"Hired successfully"})), 200
        except:
            return jsonify(error_return(500, 'Server failure, try again later!')), 500




@orders.route('/charge', methods=['POST', 'GET'])
def charge_orders():
    rave = Rave("FLWPUBK_TEST-1c33f1ea951399fbd663cb875dadd1be-X", "FLWSECK_TEST-ceb195cb2306b9b911c426f3811edce7-X", usingEnv = False)

    # mobile payload
    payload = {
    "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
    "IP":"",
      "PBFPubKey": "FLWPUBK_TEST-1c33f1ea951399fbd663cb875dadd1be-X",
  "currency": "UGX",
  "payment_type": "mobilemoneyuganda",
  "country": "UG",
  "amount": "500",
  "email": "okumujustine01@gmail.com",
  "phonenumber": "256781459239",
  "network": "UGX",
  "firstname": "Okumu",
  "lastname": "Justine",
  "orderRef": "MC_03",
  "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
    }

    try:
        res = rave.UGMobile.charge(payload)
        print(res)
        # res = rave.UGMobile.verify(res["ts"])
        # print(res)

    except RaveExceptions.TransactionChargeError as e:
        print(e.err)
        print(e.err["flwRef"])

    except RaveExceptions.TransactionVerificationError as e:
        print(e.err["errMsg"])
        print(e.err["txRef"])
    return {"charge":"charge"}



@orders.route('/make/payment', methods=['POST', 'GET'])
def make_payment():
    # https://www.easypay.co.ug/api/
    return {"coool":"cool"}