
from app import db


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


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

    def __init__(self, role):
        self.role = role


# class UserRole(Base):
    
#     __tablename__ = 'user_role'

#     user_id = db.Column(ForeignKey('user.id'))
#     role_id = db.Column(ForeignKey('role.id'))

#     def __init__(self, user_id, role_id):
#         self.user_id = user_id
#         self.role_id = role_id
