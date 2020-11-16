
from app import db, app
from app.models import Base
from app.consultation.models import ChatMessage
from flask_jwt_extended import JWTManager
from sqlalchemy import or_, and_

jwt = JWTManager(app)

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



class InvalidToken(Base):
    __tablename__ = "invalid_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_invalid(cls, jti):
        q = cls.query.filter_by(jti=jti).first()
        return bool(q)


@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)



# functions
def getUser(uid):
    users = User.query.all()
    user = list(filter(lambda x: x.id == uid, users))[0]
    return {"id": user.id, "name": user.name, "email": user.email}


def getUnreadMessageCount(agronomist_phone, phone_num):
    chat_message_count = ChatMessage.query.filter(ChatMessage.read==0,and_(ChatMessage.sender_phone == agronomist_phone, ChatMessage.receiver_phone == phone_num)).count()
    return chat_message_count

def getAgronomists(loggedIn, phone_num):
    agronomists = User.query.filter(User.roles.any(Role.role.in_(['agronomist'])))
    if loggedIn:
        return [{"id": agronomist.id, "name": agronomist.name, "phone": agronomist.phone, "unread_count":getUnreadMessageCount(agronomist.phone, phone_num)} for agronomist in agronomists]
    else:
        return [{"id": agronomist.id, "name": agronomist.name, "phone": agronomist.phone, "unread_count":0} for agronomist in agronomists]
