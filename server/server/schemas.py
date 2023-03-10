from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class ImgSchema(BaseModel):
    img: str
    # date: 
    class Config:
        orm_mode = True

class CameraResponseSchema(BaseModel):
    id: str
    name: str
    coords: list[float] # 
    active: bool
    url: str
    img: ImgSchema
    class Config:
        orm_mode = True

class LocationSchema(BaseModel):
    date: str
    img: str

    class Config:
        orm_mode = True