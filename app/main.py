from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from app.routers.auth import router as auth_router
from app.routers.question import router as question_router
from app.routers.option import router as option_router
from app.routers.game import router as game_router
from app.routers.gamequestion import router as game_question_router
from app.routers.participation import router as participation_router
from app.routers.topic import router as topic_router
from app.routers.submission import router as submission_router

from app.admin.settings import admin

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
app.include_router(submission_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Bilimdon Clone API",
        version="0.0.1",
        description="API with JWT-based Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Admin Code

admin.mount_to(app=app)
