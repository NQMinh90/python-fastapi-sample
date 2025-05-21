# /Users/nqminh/Documents/GitHub/python-fastapi-sample/app/models/candidate_tag.py
from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class CandidateTag(Base):
    __tablename__ = "candidate_tags" # Phải khớp với tên bảng bạn đã tạo trong DB

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
