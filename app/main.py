# app/main.py
import uvicorn
from fastapi import FastAPI

from app.core.logging_conf import setup_logging
from app.core.config import settings
from app.database import engine, Base
from app.routers import auth_router, user_router

async def init_models():
    """개발 환경에서 테이블 자동 생성 (Alembic 미사용 시)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )

    # 라우터 등록
    app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
    app.include_router(user_router.router, prefix="/users", tags=["Users"])

    return app

app = create_app()

@app.on_event("startup")
async def on_startup():
    await init_models()  # 테이블 자동 생성 (개발용)

# terminal : uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
