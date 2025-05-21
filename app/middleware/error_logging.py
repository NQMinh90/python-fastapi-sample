import traceback
import json
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp
from fastapi import status # Để lấy mã lỗi HTTP
from sqlalchemy.ext.asyncio import AsyncSession # Đảm bảo import AsyncSession
from app.db.logging_session import LoggingSessionLocal # Session cho LoggingDB
from app.models.error_log import ErrorLog

def _get_tenant_code_from_host(host: str | None) -> str | None:
    """
    Hàm helper đơn giản để cố gắng trích xuất tenant_code từ host.
    Lưu ý: Middleware chạy sớm, trước khi các dependency của FastAPI được giải quyết,
    nên chúng ta không thể dùng get_tenant_code_from_request dependency ở đây.
    """
    if not host:
        return None
    parts = host.split(".")
    # Điều kiện này có thể cần điều chỉnh tùy theo cấu trúc domain của bạn
    if len(parts) > 1 and parts[0] not in ["localhost", "127", "www"]:
        # Heuristic đơn giản để tránh lấy phần đầu của IP làm tenant code
        is_ip_part = parts[0].isdigit() and len(parts) >= 4 and all(p.isdigit() for p in parts[:4])
        if not is_ip_part:
            return parts[0]
    return None

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logging_db = None
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Lấy thông tin lỗi
            error_message_str = str(e)
            traceback_str = traceback.format_exc()
            tenant_code = _get_tenant_code_from_host(request.headers.get("host"))

            # Lấy thông tin request
            request_body_bytes = await request.body() # Đọc body một lần
            request_body_str = None
            try:
                # Cố gắng decode body thành text, nếu không được thì ghi là binary/undecodable
                request_body_str = request_body_bytes.decode('utf-8')
            except UnicodeDecodeError:
                request_body_str = "[Binary Body or Undecodable]"

            log_entry_data = {
                "tenant_code": tenant_code,
                "request_url": str(request.url),
                "request_method": request.method,
                "request_headers": dict(request.headers),
                "request_body": request_body_str, # Cân nhắc về bảo mật và kích thước
                "error_message": error_message_str,
                "traceback": traceback_str,
                "status_code_returned": status.HTTP_500_INTERNAL_SERVER_ERROR # Mặc định cho lỗi chưa bắt được
            }

            try:
                # logging_db = LoggingSessionLocal()                
                # log_entry = ErrorLog(**log_entry_data)
                # logging_db.add(log_entry)
                # logging_db.commit()
                async with LoggingSessionLocal() as logging_db: # Cách mới với AsyncSession
                    log_entry = ErrorLog(**log_entry_data)
                    logging_db.add(log_entry)
                    await logging_db.commit() # Commit với AsyncSession                
            except Exception as log_db_e:
                # Nếu không ghi log vào DB được thì in ra console
                print(f"CRITICAL: Failed to log error to LoggingDB: {log_db_e}")
                print(f"Original error details: {log_entry_data}")
            finally:
                if logging_db:
                    logging_db.close()
            
            # Sau khi log, trả về một response lỗi chung.
            # Hoặc bạn có thể `raise e` để cho phép các exception handler khác của FastAPI xử lý
            # việc tạo response. Việc re-raise thường tốt hơn để không ghi đè các handler khác.
            raise e # Re-raise để FastAPI xử lý response cuối cùng