from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.domain.api import api_router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(api_router)


def make_middlewares() -> list[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]

    return middlewares


def create_app() -> FastAPI:
    app_ = FastAPI(
        default_response_class=ORJSONResponse,
        middleware=make_middlewares(),
    )

    init_routers(app_)

    # 실행 : uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # app_.add_exception_handler() # TODO: 추후 exception handler 추가 

    return app_


app = create_app()
