# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Boilerplate (Async)"
    PROJECT_VERSION: str = "0.1.0"

    DB_USER: str
    DB_PASSWORD: str 
    DB_HOST: str 
    DB_PORT: str 
    DB_NAME: str 

    SECRET_KEY: str 
    ALGORITHM: str 

    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int 

    @property
    def ASYNC_DATABASE_URL(self):
        url = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        print(f"ASYNC_DATABASE_URL: {url}")  # 디버깅용 출력
        return url

    model_config = SettingsConfigDict(env_file=f"{PROJECT_DIR}/.env", case_sensitive=True)

settings = Settings()
