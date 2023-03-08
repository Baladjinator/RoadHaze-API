from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sio = SocketIO(app)

@sio.on('connect')
def connect():
    print('Client connected')

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=5000)