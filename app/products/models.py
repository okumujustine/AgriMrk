from app import db, ma
from app.models import Base


class Product(Base):
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    vendor = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('product_category', lazy=True))
    image_one = db.Column(db.String(200), nullable=False, default = 'image.jpg')
    image_two = db.Column(db.String(200), nullable=False, default = 'image.jpg')
    image_three = db.Column(db.String(200), nullable=False, default = 'image.jpg')

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(Base):
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name