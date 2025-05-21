from typing import Optional
from pydantic import BaseModel

# Schemas cho User
class UserBase(BaseModel):
    email: str # Sử dụng email làm username
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel): # Cho phép cập nhật từng phần
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

class UserSchema(UserBase): # Schema cho response, không bao gồm hashed_password
    id: int
    # hashed_password không được liệt kê ở đây, nên sẽ không được trả về

    class Config:
        from_attributes = True