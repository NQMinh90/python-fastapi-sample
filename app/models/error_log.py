from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func # Để lấy thời gian hiện tại từ server DB

from app.db.base_class import Base # Sử dụng cùng Base hoặc một Base riêng nếu cần

class ErrorLog(Base):
    # Quan trọng: Nếu bạn dùng DB-First, bạn sẽ tự tạo bảng này trong LoggingDB.
    # __tablename__ này phải khớp với tên bảng bạn tạo.
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    tenant_code = Column(String(255), nullable=True, index=True) # Nếu có thể xác định
    request_url = Column(String(2048), nullable=True)
    request_method = Column(String(10), nullable=True)
    request_headers = Column(JSON, nullable=True) # Hoặc Text
    request_body = Column(Text, nullable=True) # Cẩn thận với dữ liệu nhạy cảm
    status_code_returned = Column(Integer, nullable=True) # Mã HTTP status thực tế trả về cho client
    error_message = Column(Text, nullable=True)
    traceback = Column(Text, nullable=True)