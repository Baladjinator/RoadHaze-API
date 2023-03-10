from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class ImgSchema(BaseModel):
    img: str
    date: str

    class Config:
        orm_mode = True

class CameraResponseSchema(BaseModel):
    id: str
    name: str
    coords: list[float] # 
    active: bool
    ip: str
    img: ImgSchema
    class Config:
        orm_mode = True

class LocationResponseSchema(BaseModel):
    cameras: list[CameraResponseSchema]

    class Config:
        orm_mode = True

class LocationRequestSchema(BaseModel):
    lon: float
    lan: float

    class Config:
        orm_mode = True