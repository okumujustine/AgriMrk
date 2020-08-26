from app import db, ma

class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'orders', 'customer.name')

orders_schema = OrdersSchema(many=True)