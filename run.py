# Run a test server.
from app import app
from flask_cors import CORS
from app import socketio

CORS(app)

if __name__== '__main__':
    # ssl_context='adhoc' - to use ssl
    socketio.run(app, debug=True)
