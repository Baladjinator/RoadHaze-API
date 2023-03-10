from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from bson import BSON
from .. import db
from .. import schemas
from bson.son import SON
import geopy.distance

router = APIRouter(
    prefix='/location',
    tags=['Location']
)

@router.post('/nearby')
def getNearby(request: schemas.LocationRequestSchema):
    responseList = []
    clientCoords = (request.lat, request.lon)
    
    for doc in db.Camera.find():
        camCoords = (doc['lat'], doc['lon'])
        distance = geopy.distance.distance(clientCoords, camCoords).km
        if distance <= request.radius / 1000:
            responseList.append({
                'id': str(doc['_id']),
                'name': doc['name'],
                'lat': doc['lat'],
                'lon': doc['lon'],
                'image': {
                    'img': doc['image']['img'],
                    'date': doc['image']['date'],
                    'status': doc['image']['status']
                }
            })
    return JSONResponse(status_code=status.HTTP_200_OK, content=responseList)