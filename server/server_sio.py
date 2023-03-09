import socketio
import os
import motor.motor_asyncio


sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[], # the fastapi app will handle CORS
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client.rcnetwork

@sio.event
async def connect(sid):
    print('connect ', sid)

@sio.on('frame')
async def frame(sid, data):
    print('frame ', sid, data)

@sio.on('init_cam', namespace='/cam')
async def init_cam(sid, data):
    if data is None or data.get('_id') is None:
        
        db.cameras.insert_one({
            
        })

        await sio.emit('new_cam', namespace='/cam')

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)
