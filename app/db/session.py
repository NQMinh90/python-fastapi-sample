from typing import AsyncGenerator # Sử dụng AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Import các thành phần async
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine_args = {} 

if "mysql+aiomysql" in settings.CENTRAL_DATABASE_URL.lower():
    engine_args = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }
elif "sqlite+aiosqlite" in settings.CENTRAL_DATABASE_URL.lower(): # Nếu dùng SQLite async
    # engine_args["connect_args"] = {"check_same_thread": False} # Không cần cho aiosqlite
    pass

central_engine = create_async_engine(settings.CENTRAL_DATABASE_URL, **engine_args)
CentralSessionLocal = sessionmaker(
    bind=central_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency này không còn được sử dụng trực tiếp nếu get_central_db_session được dùng thay thế
# get_central_db_session sẽ được cập nhật trong app/dependencies/tenant.py
# def get_db() -> Generator[SQLAlchemySession, None, None]:
#     db = SessionLocal()
#     try: