from fastapi import FastAPI
import uvicorn
from server.routes import users, cameras

app = FastAPI()

app.include_router(users.router)   
app.include_router(cameras.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9999)