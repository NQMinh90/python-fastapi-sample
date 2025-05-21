from typing import Optional
from pydantic import BaseModel

# Schemas cho Item (ví dụ)
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass # Không có trường nào thêm khi tạo

class ItemUpdate(BaseModel): # Cho phép cập nhật từng phần
    title: Optional[str] = None
    description: Optional[str] = None

class ItemInDBBase(ItemBase):
    id: int

    class Config:
        from_attributes = True # Cho Pydantic 2.x (thay cho orm_mode)

class ItemSchema(ItemInDBBase): # Schema dùng cho response API
    pass