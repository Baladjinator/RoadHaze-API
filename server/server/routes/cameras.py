from fastapi import APIRouter, status, HTTPException, Request
from .. import db
from fastapi.responses import JSONResponse

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Camera already exists')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(r.inserted_id)})

@router.post('/cam_image')
async def getCamImage(request: Request):
    jsonObj = await request.json()
    r = db.Camera.update_one({'_id': jsonObj.get('id')}, {'$set': {'image': jsonObj.get('image'), 'date': jsonObj.get('date')}})

# TODO: check if camera is active
