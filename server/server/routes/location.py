from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pymongo import SON
from .. import db
from .. import schemas

router = APIRouter(
    prefix='/location',
    tags=['Location']
)

router.get('/nearby')
def getNearby(request: schemas.LocationRequestSchema):
    responseList = []
    for doc in db.Camera.find({"loc" : SON([("$near", { "$geometry" : SON([("type", "Point"), ("coordinates", [request.get('lon'), request.get('lan')])])}), ("$maxDistance", 10000)])}):
        responseList.append(
            {
                'id': str(doc.get('_id')),
                'name': doc.get('name'),    
                'coords': doc.get('loc').get('coordinates'),
                'active': doc.get('enabled'),
                'img': {
                    'img': doc.get('image').get('img'),
                    'date': doc.get('image').get('date'),
                    'status': doc.get('status')
                }
            }
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={'cameras': responseList})