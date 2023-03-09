from fastapi import FastAPI
import uvicorn
from server.schemas import UserSchema, CameraSchema

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/user/login")
async def login(request: UserSchema):
    user = request.dict()


@app.post("/user/signup")
async def signup():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get('/user/coords')
async def get_coords():
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=9999)