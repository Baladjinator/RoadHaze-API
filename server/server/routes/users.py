from fastapi import APIRouter, status, HTTPException, Response
from .. import schemas
from .. import db
from .. import hashing

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/login')  # 202 =
async def login(request: schemas.UserSchema):
    user = db.User.find_one({ 'email': request.email })
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    
    if not hashing.Hash.verify(request.password, user['password']):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail=f'Incorrect password')

    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post('/signup')
async def signup(request: schemas.UserSchema):
    user = db.User.find_one({ 'email': request.email })
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User already exists')
    db.User.insert_one({"email": request.email, "password": hashing.Hash.bcrypt(request.password) })
    return Response(status_code=status.HTTP_201_CREATED)
