# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

# 비동기 엔진 생성
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,  # 개발 중에는 True로 설정하여 SQL 로그를 확인할 수 있습니다.
    pool_pre_ping=True
)

# 비동기 세션 메이커
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """요청마다 비동기 DB 세션을 열고 닫는 종속성"""
    async with AsyncSessionLocal() as session:
        yield session
