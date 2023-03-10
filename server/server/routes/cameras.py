from fastapi import APIRouter, status, HTTPException, Response, Request
from .. import schemas
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
            'name': jsonObj.get('name'),
            'location': [jsonObj.get('lon'), jsonObj.get('lan')],
            'enabled': True,
            'image': None
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Camera already exists')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(r.inserted_id)})

@router.post('/cam_image')
async def getCamImage(request: Request):
    print(await request.json())