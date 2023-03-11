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
# import cv2

router = APIRouter(
    prefix='/camera',
    tags=['Cameras']
)

# no type checking due to a bug in pydantic
@router.post('/init')
async def initCam(request: Request):
    jsonObj = await request.json()

    try:
        print(jsonObj.get('lat'))
        r = db.Camera.insert_one({
            'name': jsonObj.get('name'),
            'lat': jsonObj.get('lat'),
            'lon': jsonObj.get('lon'),
            'image': None
        })
    except Exception as e:
        print(e.__str__())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.__str__())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(r.inserted_id)})

# num = 0

@router.post('/cam_image')
async def getCamImage(request: Request):
    # global num
    jsonObj = await request.json()
    objid = ObjectId(jsonObj.get('id'))

    img = base64.b64decode(jsonObj.get('img'))

    img = Image.open(io.BytesIO(img))
    img = np.array(img)

    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    convert_tensor = transforms.ToTensor()
    imgT = convert_tensor(blackAndWhiteImage)

    label = eval_for_camera(model, imgT, labels_names)
    print(label)

    r = db.Camera.update_one({'_id': objid}, {'$set': {'image': {'img': jsonObj.get('img'), 'date': jsonObj.get('date'), 'status': label}}})
    if r.modified_count == 0:
        print('no camera found')
    return Response(status_code=status.HTTP_202_ACCEPTED)
# TODO: check if camera is active
