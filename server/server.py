from fastapi import FastAPI
import uvicorn
import dotenv
import os
from server_sio import sio_app
from models import CameraDevice

dotenv.load_dotenv()

app = FastAPI()
app.mount('/ws', app=sio_app)

if __name__ == '__main__':
    uvicorn.run('server:app', host="localhost", port=9999, reload=True)