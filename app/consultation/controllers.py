from flask import Blueprint, jsonify, request
from app import socketio
from flask_socketio import SocketIO, send, emit
from sqlalchemy import or_, and_
from app import app, db

from .models import ChatThread, ChatMessage

consultation = Blueprint('consultation', __name__)

@consultation.route('/')
def index():
    return "make"


@consultation.route('/chatmessages', methods=["GET"])
def get_chat_messages():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    chat_thread = get_chat_thread(sender, receiver)

    chat_messages = get_chat_messages(chat_thread)

    return jsonify(chat_messages), 200


users = {}

@socketio.on('username', namespace="/private")
def recieve_username(username):
    users[str(username)] = request.sid


@socketio.on('private_message', namespace="/private")
def recieve_username(payload):
    try:
        reciever_id = users[str(payload['reciever'])]
    except KeyError:
        return
    reciever = payload['reciever']
    message = payload['message']
    sender = payload['sender']

    chat_thread = get_chat_thread(sender, reciever)

    has_saved_message = save_chat_message(chat_thread, sender, reciever, message)

    message_data = {
        "message": message,
        "reciever": reciever,
        "sender": sender
    }
    emit('new_private_message', message_data, room=reciever_id)


@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)
    return None




def get_chat_thread(sender, reciever):
    chat_thread = ChatThread.query.filter(or_(and_(ChatThread.sender_phone == sender, ChatThread.receiver_phone == reciever), and_(ChatThread.sender_phone == reciever, ChatThread.receiver_phone == sender))).first()
    if chat_thread is None:
        new_chat_thread = create_chat_thread(sender, reciever)
        return new_chat_thread
    else:
        return chat_thread


def create_chat_thread(sender_phone, reciever_phone):
    chat_thread = ChatThread(sender_phone=sender_phone, receiver_phone=sender_phone)
    db.session.add(chat_thread)
    db.session.commit()

    return chat_thread


def save_chat_message(thread, sender_phone, receiver_phone, message):
    chat_message = ChatMessage(thread=thread, sender_phone=sender_phone, receiver_phone=receiver_phone, message=message)
    db.session.add(chat_message)
    db.session.commit()

    return True

def get_chat_messages(thread):
    chat_message = ChatMessage.query.filter(ChatMessage.thread_id==thread.id).order_by(ChatMessage.date_created.asc()).paginate(1, 20, False)
    return [{"id": chat.id, "message":chat.message , "reciever":chat.receiver_phone , "sender": chat.sender_phone, "read": chat.read} for chat in chat_message.items]
