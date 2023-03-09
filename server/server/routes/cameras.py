from fastapi import APIRouter, status, HTTPException, Response
from .. import schemas
from .. import db

router = APIRouter(
    prefix='/camera',
    tags=['Users']
)