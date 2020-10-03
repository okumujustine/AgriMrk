
from flask import Blueprint, request, jsonify, Response
from rave_python import Rave, RaveExceptions, Misc
import secrets
from app import db

from app.orders.models import CustomerOder, CustomerHireOder
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



# CustomerHireOder -> add hire order
@orders.route('/hire/add', methods=['POST', 'GET'])
@token_required
def add_hire_orders(current_user):
    if request.method == 'POST':

        return jsonify(success_return(200,{"success":"Order created", "user":current_user})), 200

    #     cart_items = request.json['order'] 
    #     invoice_number = secrets.token_hex(5)
    #     if not cart_items:
    #         return jsonify(error_return(400, 'No order items')), 400
    #     print(cart_items)
    #     try:
    #         final_order = CustomerOder(
    #             invoice=invoice_number,
    #             status="pending",
    #             address=current_user["district"],
    #             phone=current_user["phone"],
    #             customer_id=current_user["id"],
    #             orders=cart_items
    #         )
    #         db.session.add(final_order)
    #         db.session.commit()
    #     except:
    #         return jsonify(error_return(500, 'Server failure, try again later!')), 500

    #     return jsonify(success_return(200,{"success":"Order created", "user":current_user})), 200
    # else:
    #     return jsonify({"failed":"invalid request"})




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