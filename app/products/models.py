from app import db, ma
from app.models import Base
from sqlalchemy import and_, or_


class Product(Base):
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    vendor = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=0)
    sale_type = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('product_category', lazy=True))
    category_name = db.Column(db.String(100), nullable=False)
    image_one = db.Column(db.String(200), nullable=False, default = 'image.jpg')
    image_two = db.Column(db.String(200), nullable=False, default = 'image.jpg')
    image_three = db.Column(db.String(200), nullable=False, default = 'image.jpg')

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(Base):
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


def getCategory():
    categories = Category.query.all()
    return {"categories":[{"id": i.id, "name":i.name} for i in categories]}
    

def getProductsFiltered(page_number, filter_object):
    products = Product.query.filter(Product.sale_type == "sale", Product.title.like("%" + filter_object["title"] + "%")).order_by(Product.date_created.desc()).paginate(page_number, 12, False)
    return returnProducts(products)


def getProducts(page_number):
    products = Product.query.filter_by(sale_type="sale").order_by(Product.date_created.desc()).paginate(page_number, 12, False)
    return returnProducts(products)


def getHireProducts(page_number):
    products = Product.query.filter_by(sale_type="hire").order_by(Product.date_created.desc()).paginate(page_number, 12, False)
    return returnProducts(products)

def returnProducts(products):
    return {"products":[{"id": i.id, "description":i.description, "title":i.title,
    "vendor":i.vendor, "price":i.price,"stock":i.stock, 
    "sale_type":i.sale_type, "image_one":i.image_one,"category_name":i.category.name, 
    "image_two":i.image_two, "image_three":i.image_three} for i in products.items], "current_page":products.page , "per_page":products.per_page ,"total":products.total}
