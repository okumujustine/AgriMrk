from app import db, ma

class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'orders', 'customer.name')

orders_schema = OrdersSchema(many=True)


class HireProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date_created', 'date_modified','hire_number', 'status', 'address', 'phone', 'customer_id', 'product_id', 'product_name', 'days_number', 'return_date', 'needed_date', 'given_date', 'hire_notes','customer.name')

hire_products_schema = HireProductSchema(many=True)