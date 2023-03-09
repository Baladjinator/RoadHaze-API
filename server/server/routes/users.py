from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas



router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)  # 202 =
async def login(request: schemas.UserSchema):
    pass

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: schemas.UserSchema):
    pass
