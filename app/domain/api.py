from fastapi import APIRouter

from app.domain.auth.endpoints import router as auth_router
from app.domain.user.endpoints import router as user_router


api_router = APIRouter()


@api_router.get("/", summary="Hello World", include_in_schema=False)
def index():
    return {
        "Hello": "World",
    }


# TODO. set environment variable
SWAGGER_USERNAME = "admin"
SWAGGER_PASSWORD = "gdrecord"


api_router.include_router(auth_router)
api_router.include_router(user_router)


