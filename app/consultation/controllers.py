from flask import Blueprint, request
from app import socketio
from flask_socketio import SocketIO, send, emit

consultation = Blueprint('consultation', __name__)

@consultation.route('/')
def index():
    return "make"


users = {}

@socketio.on('username', namespace="/private")
def recieve_username(username):
    users[str(username)] = request.sid
    print(users)
    print("username added")


@socketio.on('private_message', namespace="/private")
def recieve_username(payload):
    reciever_id = users[payload['reciever']]
    reciever = payload['reciever']
    message = payload['message']
    sender = payload['sender']
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