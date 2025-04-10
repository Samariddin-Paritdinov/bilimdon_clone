from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def hello():
    return "Hello"


app.include_router(signin_router)