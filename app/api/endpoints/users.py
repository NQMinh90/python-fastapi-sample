from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as SQLAlchemySession

from app.api import dependencies # Sử dụng dependencies đã tạo
from app.db.session import get_db
from app.models.schemas import UserCreate, UserSchema, UserUpdate, Msg
from app.services.impl.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=201)
async def create_user_registration(
    *,
    db: SQLAlchemySession = Depends(get_db),
    user_in: UserCreate,
    user_service: UserService = Depends(dependencies.get_user_service) # Sử dụng dependency
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
    current_user: UserSchema = Depends(dependencies.get_current_active_user),
):
    """
    Get current user.
    """
    return current_user

# Bạn có thể thêm các endpoint CRUD khác cho User ở đây nếu muốn,
# ví dụ sử dụng BaseAPIRouter hoặc viết thủ công.
# Ví dụ: GET /users/{user_id}, GET /users/, PUT /users/{user_id} (yêu cầu superuser)