from typing import AsyncGenerator # Sử dụng AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Import các thành phần async
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logging_engine_args = {}
if "mysql+aiomysql" in settings.LOGGING_DATABASE_URL.lower():
    logging_engine_args.update({
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    })
elif "sqlite+aiosqlite" in settings.LOGGING_DATABASE_URL.lower(): # Nếu dùng SQLite async
    pass

logging_engine = create_async_engine(settings.LOGGING_DATABASE_URL, **logging_engine_args)
LoggingSessionLocal = sessionmaker(
    bind=logging_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_logging_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with LoggingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise