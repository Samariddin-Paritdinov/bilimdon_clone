from typing import Union
import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.routers.question import router as question_router

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth_router)
app.include_router(question_router)