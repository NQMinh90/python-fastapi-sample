# /Users/nqminh/Documents/GitHub/python-fastapi-sample/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users" # Phải khớp với tên bảng bạn tạo trong DB

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
