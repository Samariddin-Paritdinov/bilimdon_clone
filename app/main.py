from fastapi import FastAPI

from app.routers.auth import router as signin_router
app = FastAPI()

@app.get("/")
async def hello():
    return "Hello"


app.include_router(signin_router)