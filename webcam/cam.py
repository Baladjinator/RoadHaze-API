import cv2
import base64
import asyncio
from datetime import datetime
import json

import requests

conf = None

class CameraCapture:
    camera = cv2.VideoCapture(0)

    async def snap(self):
        success, img = self.camera.read()
        if not success:
            raise Exception('Failed to capture image')
        else:
            cv2.imwrite('pic.jpg', img=img)

            ret, buffer = cv2.imencode('.png', img)
            img = buffer.tobytes()
            
            #return base64.b64encode(b'Content-Type: image/jpeg\r\n\r\n'+ img + b'\r\n')
            return base64.b64encode(img)
            

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
        'lan': conf.get('lan')
    }
    
    # TODO: FIX THIS
    r = requests.post(conf.get('s_url_init') , data=json.dumps(jsonObj), headers=headers)
    
    print(type(conf.get('lon')))
    
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
            "date": now.strftime("%d/%m/%Y %H:%M:%S"),
            "img": str(await camera.snap())
        })
        await asyncio.sleep(__seconds)

init()

a = asyncio.get_event_loop()
a.create_task(snap(10))
a.run_forever()