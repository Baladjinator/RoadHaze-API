from fastapi import APIRouter, status, HTTPException, Response
from .. import schemas
from .. import db
from .. import hashing

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)  # 202 =
async def login(request: schemas.UserSchema):
    user = db.User.find_one({ 'email': request.email })
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    if hashing.Hash.verify(user['password'], request.password):
        return HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail=f'Incorrect password')

    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: schemas.UserSchema):
    user = db.User.find_one({ 'email': request.email })
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User already exists')
    hashed_password = hashing.Hash.bcrypt(request.password)
    db.User.insert_one({"email": request.email, "password": hashed_password})
    return Response(status_code=status.HTTP_201_CREATED)
