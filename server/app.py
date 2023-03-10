from fastapi import FastAPI
import uvicorn
from server.routes import users, cameras

from fastapi.middleware.cors import CORSMiddleware


# TODO: Add JWT authentication

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return 'Hello, World!'

app.include_router(users.router)   
app.include_router(cameras.router)

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=9009, reload=True)