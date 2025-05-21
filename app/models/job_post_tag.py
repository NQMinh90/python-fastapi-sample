from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class JobPostTag(Base):
    __tablename__ = "job_post_tags" # Phải khớp với tên bảng bạn đã tạo trong DB

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

# Đảm bảo bảng 'job_post_tags' đã được tạo trong cơ sở dữ liệu của các tenant
# với cột 'id' là AUTO_INCREMENT PRIMARY KEY.