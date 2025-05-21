from typing import AsyncGenerator, Optional
from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession # Sử dụng AsyncSession
from sqlalchemy import select # Import select cho truy vấn async


from app.db.session import CentralSessionLocal # Session cho Central DB
from app.models.tenant import Tenant as TenantModel
from app.core.config import settings # Import settings


# Dependency để lấy session của Central DB
async def get_central_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with CentralSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# Dependency để trích xuất tenant_code từ request host
async def get_tenant_code_from_request(request: Request) -> str:
    if settings.APP_ENV == "Development":
        if settings.DEV_TENANT_CODE:
            return settings.DEV_TENANT_CODE
        else:
            # Nếu APP_ENV là Development nhưng DEV_TENANT_CODE không được set, báo lỗi hoặc có hành vi mặc định khác
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Development mode is active but DEV_TENANT_CODE is not set in settings."
            )

    # Logic cho APP_ENV = "Production" (hoặc bất kỳ giá trị nào khác "Development")
    host = request.headers.get("host")
    if not host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Host header is missing."
        )

    parts = host.split(".")
    # Logic trích xuất tenant_code từ phần đầu của host.
    # Ví dụ: 'tenant1.example.com' -> 'tenant1'
    if len(parts) > 1: # Cần ít nhất dạng subdomain.domain
        # Kiểm tra xem phần đầu có phải là một phần của IP address không (heuristic đơn giản)
        is_ip_part = parts[0].isdigit() and len(parts) >= 4 and all(p.isdigit() for p in parts[:3]) # Kiểm tra 3 phần đầu nếu có 4 phần
        if not is_ip_part and parts[0].lower() not in ["www", "app", "api"]: # Bỏ qua các subdomain phổ biến không phải tenant
            return parts[0]

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not determine tenant code from host. Expected format: tenant_code.domain.com"
    )


# Dependency để lấy connection string của tenant từ Central DB
async def get_tenant_db_connection_string(
    tenant_code: str = Depends(get_tenant_code_from_request),
    central_db: AsyncSession = Depends(get_central_db_session)
) -> str:
    statement = select(TenantModel).where(TenantModel.tenant_code == tenant_code)
    result = await central_db.execute(statement)
    tenant_info = result.scalar_one_or_none()
    if tenant_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant '{tenant_code}' not found or not configured."
        )
    if not tenant_info.db_connection_string:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Connection string for tenant '{tenant_code}' is not configured."
        )
    return tenant_info.db_connection_string

# *   `get_central_db_session`: Cung cấp session để tương tác với Central DB.
# *   `get_tenant_code_from_request`: Trích xuất `tenant_code` từ header `Host` của request. Logic này có thể cần điều chỉnh tùy theo cấu trúc domain của bạn và cách bạn xử lý môi trường dev (ví dụ: `localhost`).
# *   `get_tenant_db_connection_string`: Sử dụng `tenant_code` và `central_db` session để truy vấn bảng `tenants` và lấy ra connection string của tenant đó.