from sqlalchemy import Column, String, Integer
from app.db.base_class import Base # Đảm bảo Base được import đúng

class Tenant(Base):
    __tablename__ = "tenants" # Tên bảng trong central DB

    id = Column(Integer, primary_key=True, index=True)
    tenant_code = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True) # Tên tenant, ví dụ: "Công ty A"
    db_connection_string = Column(String(512), nullable=False) # Connection string tới DB của tenant
    # Bạn có thể thêm các trường khác như is_active, created_at, v.v.