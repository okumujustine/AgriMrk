
from app import db, app
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.BigInteger, db.ForeignKey('user.id')),
    db.Column('role_id', db.BigInteger, db.ForeignKey('role.id'))
)

class User(Base):

    __tablename__ = 'user'

    country = db.Column(db.String(128),  nullable=False)
    region = db.Column(db.String(128),  nullable=False)
    district = db.Column(db.String(128),  nullable=False)
    phone = db.Column(db.BigInteger(),  nullable=False)
    name = db.Column(db.String(128),  nullable=False)
    email = db.Column(db.String(128),  nullable=True, unique=True)
    password = db.Column(db.String(192),  nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    roles = db.relationship('Role', secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, country, region, district, phone, name, email, password, status):

        self.country = country
        self.region = region
        self.district = district
        self.phone = phone
        self.name = name
        self.email = email
        self.password = password
        self.status = status

    def __repr__(self):
        return '<User %r>' % (self.name)


class Role(Base):

    __tablename__ = 'role'
    
    role = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, role):
        self.role = role
