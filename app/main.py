from fastapi import FastAPI, Request

from app.routers.auth import router as auth_router
from app.routers.question import router as question_router
from app.routers.option import router as option_router
from app.routers.game import router as game_router
from app.routers.gamequestion import router as game_question_router
from app.routers.participation import router as participation_router
from app.routers.topic import router as topic_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(auth_router)
app.include_router(question_router)
app.include_router(option_router)
app.include_router(game_router)
app.include_router(game_question_router)
app.include_router(participation_router)
app.include_router(topic_router)





