from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class LocationRequestSchema(BaseModel):
    lon: float
    lat: float
    radius: float

    class Config:
        orm_mode = True