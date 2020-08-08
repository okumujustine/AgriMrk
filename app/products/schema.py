from app import db, ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'vendor', 'price', 'discount', 'stock', 'category.name','image_one', 'image_two', 'image_three')

products_schema = ProductSchema(many=True)