from typing import Union
import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.routers.question import router as question_router
from app.routers.option import router as option_router
from app.routers.game import router as game_router
from app.routers.gamequestion import router as game_question_router


app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth_router)
app.include_router(question_router)
app.include_router(option_router)
app.include_router(game_router)
app.include_router(game_question_router)


