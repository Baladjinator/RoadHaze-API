from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    password: str
    bookmarks: list

    class Config:
        orm_mode = True

class CameraBaseSchema(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    active: bool
    url: str

    class Config:
        orm_mode = True
