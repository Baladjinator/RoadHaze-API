from fastapi import APIRouter, status, HTTPException, Response
from .. import db
from .. import schemas

router = APIRouter(
    prefix='/location',
    tags=['Location']
)

router.get('/nearby')
def getNearby(request: schemas.LocationSchema):
    cameras = db.Camera.find({ 'location': request.location })
    