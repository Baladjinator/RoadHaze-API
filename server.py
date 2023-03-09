from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from python_dotenv import load_dotenv
from datetime import datetime, timedelta
from functools import wraps
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = load_dotenv('.env').get('SECRET_KEY')
jwt = JWTManager(app)
sio = SocketIO(app)


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username', None)


@app.route('/login')
def login():
    return 'Hello world'

@sio.on('connect')
def connect():
    print('Client connected')

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=9999)