from flask import Blueprint


consultation = Blueprint('consultation', __name__)

@consultation.route('/')
def index():
    return "make"