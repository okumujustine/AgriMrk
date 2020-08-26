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

