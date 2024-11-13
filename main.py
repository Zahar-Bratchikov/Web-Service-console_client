import uvicorn
from fastapi import FastAPI
from web_app import api_router
from uvicorn import Config, Server

app = FastAPI()
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
