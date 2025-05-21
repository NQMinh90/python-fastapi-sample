from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship # Nếu có quan hệ
from app.db.base_class import Base

class Item(Base):
    __tablename__ = "items" # Phải khớp với tên bảng bạn tạo trong DB

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    # owner_id = Column(Integer, ForeignKey("users.id")) # Ví dụ nếu có quan hệ với User
    # owner = relationship("User", back_populates="items")
