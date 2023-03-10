import cv2
import base64
import asyncio
from datetime import datetime
from picamera import PiCamera
import json
import imutils

import requests

conf = None

class CameraCapture:
    camera = cv2.VideoCapture(-1, cv2.CAP_V4L2)
    camera.set(3, 480)
    camera.set(4, 360)
    async def snap(self):
        success, img = self.camera.read()
        
        if not success:
            raise Exception('Failed to capture image')
        else:
            cropimg = img[:, 120: 360]
            
            # cv2.imwrite('pic2.jpg', img=cropimg)

            ret, buffer = cv2.imencode('.png', cropimg)
            cropimg = buffer.tobytes()
            
            b64_img = base64.b64encode(cropimg)

            return b64_img
def init():
    global conf
    with open('cam-conf.json', 'r') as f:
        conf = json.load(f)
    
    if conf.get('s_url_init') is None or conf.get('s_url') is None:
        raise Exception('Invalid server address')
    
    headers = {'Content-Type': 'application/json'}
    
    jsonObj = {
        'name': conf.get('name'),
        'lon': conf.get('lon'),
        'lat': conf.get('lat')
    }
    
    r = requests.post(conf.get('s_url_init') , json=jsonObj, headers=headers)
    
    
    if r.status_code == 504:
        raise Exception('Connection to server timed out')
    
    conf.update(r.json())
    
    with open('cam-conf.json', 'w') as f:
        json.dump(conf, f)

    
async def snap(__seconds: float):
    while True:
        print('snap')
        now = datetime.now()
        
        camera = CameraCapture()
        
        requests.post(conf.get('s_url'), json = {
            "id": conf.get('id'),
            "date": now.strftime("%d/%m/%Y %H:%M:%S"),
            "img": (await camera.snap()).decode('utf-8')
        })
        await asyncio.sleep(__seconds)

init()

a = asyncio.get_event_loop()
a.create_task(snap(2))
a.run_forever()
