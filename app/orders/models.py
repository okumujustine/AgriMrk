from app import db, app
import sqlalchemy.types as types

from app.models import Base
import json


class EncodeOrderItem(types.TypeDecorator):

    impl = types.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOder(Base):
    invoice = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger(),  nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    customer = db.relationship('User',backref=db.backref('user_order', lazy=True))
    orders = db.Column(EncodeOrderItem)

    def __repr__(self):
        return '<CustomerOder %r>' % self.invoice



class CustomerHireOder(Base):
    hire_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger(),  nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    customer = db.relationship('User',backref=db.backref('user_hire_order', lazy=True))
    product_id = db.Column(db.Integer(),  nullable=False)
    product_name = db.Column(db.String(),  nullable=False)
    days_number = db.Column(db.Integer(),  nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    needed_date = db.Column(db.DateTime,  nullable=False)
    given_date = db.Column(db.DateTime,  nullable=True)
    hire_notes = db.Column(db.String(50), nullable=True)





def getHireOrdersList(page_number, customer_id):
    hire_requests = CustomerHireOder.query.filter_by(customer_id=customer_id).order_by(CustomerHireOder.date_created.desc()).paginate(page_number, 8, False)
    return returnHireOrders(hire_requests)


def getHireOrdersListFiltered(page_number, customer_id, filter_object):
    hire_requests = CustomerHireOder.query.filter(CustomerHireOder.customer_id==customer_id, CustomerHireOder.product_name.like("%" + filter_object["title"] + "%")).order_by(CustomerHireOder.date_created.desc()).paginate(page_number, 8, False)
    return returnHireOrders(hire_requests)

def returnHireOrders(hire_requests):
    return {"hire_requests_products":[{ "id":i.id , 'date_created':i.date_created, 'date_modified':i.date_modified,'hire_number':i.hire_number, 'status':i.status, 'address':i.address, 'phone':i.phone, 'customer_id':i.customer_id, 'product_id':i.product_id, 'product_name':i.product_name, 'days_number':i.days_number, 'return_date':i.return_date, 'needed_date':i.needed_date, 'given_date':i.given_date, 'hire_notes':i.hire_notes,'customer_name':i.customer.name} for i in hire_requests.items], "current_page":hire_requests.page , "per_page":hire_requests.per_page ,"total":hire_requests.total}