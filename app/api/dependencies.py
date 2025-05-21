from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session as SQLAlchemySession

from app.core.config import settings
from app.db.session import get_db
from app.models.schemas import TokenData, UserSchema, UserInDBBase as UserInDB
from app.services.impl.user_service import UserService
from app.repositories.impl.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login" # Sửa thành /auth/login cho phù hợp
)

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=repo)

async def get_current_user(
    db: SQLAlchemySession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserInDB: # Trả về UserInDB để có thể dùng trong service, API sẽ convert sang UserSchema
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await user_service.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user # Trả về đối tượng UserInDB

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_superuser(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user