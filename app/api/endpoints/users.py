# /Users/nqminh/Documents/GitHub/python-fastapi-sample/app/api/endpoints/users.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession # Sử dụng AsyncSession
from app.dependencies import get_db, get_user_service, get_current_active_user
from app.models.schemas import UserCreate, UserSchema, UserUpdate, Msg
from app.services.impl.user_service import UserService # Vẫn cần cho type hinting nếu bạn dùng

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=201)
async def create_user_registration(
    *,
    db: AsyncSession = Depends(get_db), # Sử dụng get_db đã import
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service) # Sử dụng get_user_service đã import
):
    """
    Create new user without needing authentication.
    """
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    created_user = await user_service.create_user(db, obj_in=user_in)
    return created_user


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    # current_user được type hint là UserSchema vì API trả về UserSchema
    # get_current_active_user trả về UserInDB, FastAPI sẽ tự chuyển đổi
    current_user: UserSchema = Depends(get_current_active_user), # Sử dụng get_current_active_user đã import
):
    """
    Get current user.
    """
    return current_user

# Bạn có thể thêm các endpoint CRUD khác cho User ở đây nếu muốn,
# ví dụ sử dụng BaseAPIRouter hoặc viết thủ công.
# Ví dụ: GET /users/{user_id}, GET /users/, PUT /users/{user_id} (yêu cầu superuser)