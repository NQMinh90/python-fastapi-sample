from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
# from pydantic import PostgresDsn, validator # Bỏ comment nếu dùng PostgresDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "3-Tier FastAPI Project"
    API_V1_STR: str = "/api/v1"

    # Database settings (ví dụ, chỉnh sửa nếu cần)
    # Mặc định sẽ dùng SQLite nếu không có biến môi trường
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./default_app.db"

    # JWT Settings
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE_CHANGE_ME" # << RẤT QUAN TRỌNG: Thay đổi key này!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 phút
    
    # POSTGRES_SERVER: str = "localhost"
    # POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "password"
    # POSTGRES_DB: str = "app_db"
    # DATABASE_URL: Optional[PostgresDsn] = None

    # @validator("DATABASE_URL", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql", user=values.get("POSTGRES_USER"), password=values.get("POSTGRES_PASSWORD"), host=values.get("POSTGRES_SERVER"), path=f"/{values.get('POSTGRES_DB') or ''}",)

    class Config:
        case_sensitive = True
        env_file = ".env" # Tải biến môi trường từ file .env

settings = Settings()