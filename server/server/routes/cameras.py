from fastapi import APIRouter, status, HTTPException, Request, Response
from .. import db
from fastapi.responses import JSONResponse
from bson import ObjectId
from ..model.model import model, eval_for_camera, convert_tensor, labels_names
import base64
import io
from PIL import Image
import numpy as np
from torchvision import transforms

router = APIRouter(
    prefix='/camera',
    tags=['Cameras']
)

# no type checking due to a bug in pydantic
@router.post('/init')
async def initCam(request: Request):
    jsonObj = await request.json()

    try:
        r = db.Camera.insert_one({
            'ip': request.client.host,
            'name': jsonObj.get('name'),
            'loc': {
                'type': 'Point',
                'coordinates': [jsonObj.get('lon'), jsonObj.get('lan')]
            },
            'enabled': True,
            'image': None
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.__str__())
    print(r.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(r.inserted_id)})

num = 0

@router.post('/cam_image')
async def getCamImage(request: Request):
    global num
    jsonObj = await request.json()
    objid = ObjectId(jsonObj.get('id'))

    img = base64.b64decode(jsonObj.get('img'))
    
    with open('test' + str(num) + '.png', 'wb') as f:
        f.write(img)
        num += 1

    img = Image.open(io.BytesIO(img))
    img = np.array(img)

    convert_tensor = transforms.ToTensor()
    imgT = convert_tensor(img)

    label = eval_for_camera(model, imgT, labels_names)
    print(label)
    r = db.Camera.update_one({'_id': objid}, {'$set': {'image': {'img': jsonObj.get('img'), 'date': jsonObj.get('date'), 'status': label}}})
    if r.modified_count == 0:
        print('no camera found')
    return Response(status_code=status.HTTP_202_ACCEPTED)
# TODO: check if camera is active
