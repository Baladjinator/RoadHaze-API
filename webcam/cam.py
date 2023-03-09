from socketio import AsyncClient
import json
import cv2
from threading import Timer
import asyncio
from util import get_location

asio = AsyncClient()
cam = cv2.VideoCapture(0) # get the camera object
config = None
# async def periodic():
#     while True:
#         print('periodic')
#         await asio.sleep(1)

# async def genFrames():
#     while True:
#         await asio.emit('frame', {'frame': 'frame'})
#         await asyncio.sleep(5)

@asio.event
async def connect():
    print('device connected: ' + asio.sid)

@asio.on('new_cam')
async def new_cam(data):
    with open('cam-idconfig.json', 'w') as f:
        json.dump(data, f)

@asio.on('abort')
async def abort():
    pass

@asio.event
async def disconnect():
    print('device disconnected: ' + asio.sid)

async def main():
    global config
    with open('cam-idconfig.json') as f:
        config = json.load(f)

    coords = get_location()
    data = {
        '_id': config.get('_id') if config else None,
        'name': config.get('name') if config else None,
        'lat': coords.get('lat'),
        'lon': coords.get('lon'),
    } 

    await asio.connect('ws://localhost:9999', socketio_path='/ws/socket.io', auth=auth)
    await asio.emit('init_cam', data=data, namespace='/cam')
    await asio.wait()

asyncio.run(main())