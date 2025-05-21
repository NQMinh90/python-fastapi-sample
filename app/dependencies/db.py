from typing import AsyncGenerator, Dict # Sử dụng AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Import các thành phần async
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dependencies.tenant import get_tenant_db_connection_string # Dependency mới
from app.core.config import settings # Để lấy engine_args nếu cần

# Cache để lưu trữ engine và sessionmaker cho từng tenant connection string
# Key: tenant_connection_string, Value: sqlalchemy.ext.asyncio.AsyncEngine
_tenant_engines: Dict[str, any] = {}
# Key: tenant_connection_string, Value: sqlalchemy.orm.sessionmaker
_tenant_session_locals: Dict[str, sessionmaker] = {}

    # Các engine_args có thể cần cho MySQL (thường ít hơn SQLite)
MYSQL_ENGINE_ARGS = {
    "pool_recycle": 3600, # Ví dụ: tái sử dụng connection sau 1 giờ
    "pool_pre_ping": True # Kiểm tra connection trước khi sử dụng từ pool
    # Đối với aiomysql, bạn có thể cần các args khác hoặc không cần nhiều như driver đồng bộ
}

# Dependency để lấy DB session
async def get_db( # Hàm này giờ là async
    tenant_conn_str: str = Depends(get_tenant_db_connection_string)
) -> AsyncGenerator[AsyncSession, None]: # Trả về AsyncSession
    
    current_engine_args = {}
    # Kiểm tra driver trong connection string để áp dụng args phù hợp
    if "mysql+aiomysql" in tenant_conn_str.lower():
        current_engine_args = MYSQL_ENGINE_ARGS
    elif "sqlite+aiosqlite" in tenant_conn_str.lower(): # Nếu bạn dùng aiosqlite cho SQLite async
        # current_engine_args = {} # aiosqlite thường không cần connect_args đặc biệt
        pass

    if tenant_conn_str not in _tenant_engines:
        # Sử dụng create_async_engine
        _tenant_engines[tenant_conn_str] = create_async_engine(tenant_conn_str, **current_engine_args)
        # Tạo sessionmaker cho AsyncSession
        _tenant_session_locals[tenant_conn_str] = sessionmaker(
            bind=_tenant_engines[tenant_conn_str],
            class_=AsyncSession, # Chỉ định class là AsyncSession
            expire_on_commit=False # Quan trọng cho async
        )

    TenantSessionLocal = _tenant_session_locals[tenant_conn_str]
    
    # Sử dụng 'async with' để quản lý vòng đời của AsyncSession
    async with TenantSessionLocal() as session:
        try:
            yield session
            # Commit có thể được thực hiện ở đây nếu không có lỗi,
            # hoặc để service/repository tự quản lý transaction.
            # await session.commit() # Tùy chọn: commit ở cuối nếu không có lỗi
        except Exception:
            await session.rollback() # Rollback nếu có lỗi
            raise
        # Session sẽ tự động được đóng bởi 'async with'
        # không cần gọi session.close() một cách tường minh trong finally