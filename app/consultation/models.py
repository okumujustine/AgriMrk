
from app import db, app
from app.models import Base

class ChatMessage(Base):

    __tablename__ = 'chat_message'

    thread_id = db.Column(db.BigInteger, db.ForeignKey("chat_thread.id"))
    thread = db.relationship('ChatThread', foreign_keys=thread_id)
    sender_phone = db.Column(db.BigInteger(),  nullable=False)
    receiver_phone = db.Column(db.BigInteger(),  nullable=False)
    message = db.Column(db.String(256))
    read = db.Column(db.Integer(), nullable=False, default=0)


class ChatThread(Base):

    __tablename__ = 'chat_thread'

    sender_phone = db.Column(db.BigInteger(),  nullable=False)
    receiver_phone = db.Column(db.BigInteger(),  nullable=False)

    def __init__(self, sender_phone, receiver_phone):

        self.sender_phone = sender_phone
        self.receiver_phone = receiver_phone

    def __repr__(self):
        return '<ChatThread %r>' % (self.sender_phone)