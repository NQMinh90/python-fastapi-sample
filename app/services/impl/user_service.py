from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession # Sử dụng AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User as UserModel # Import SQLAlchemy model
from app.models.schemas import UserCreate, UserUpdate # Giữ Pydantic schemas
from app.repositories.impl.user_repository import UserRepository
from app.services.base_service import BaseService

class UserService(BaseService[UserRepository, UserModel, UserCreate, UserUpdate]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(repository=user_repository)
        self.user_repository = user_repository # Gán lại để có type hinting tốt hơn

    async def create_user(self, db: AsyncSession, *, obj_in: UserCreate) -> UserModel:
        """
        Tạo người dùng mới. Mật khẩu sẽ được băm.
        """
        hashed_password = get_password_hash(obj_in.password)
        
        # Chuẩn bị dữ liệu để tạo UserModel
        user_data_for_db = obj_in.model_dump(exclude={"password"})
        user_data_for_db["hashed_password"] = hashed_password       
        
        # Tạo UserModel trực tiếp từ dữ liệu đã chuẩn bị
        db_user_model = UserModel(**user_data_for_db)
      
        created_user = await self.user_repository.create_db_user_with_hashed_password(db, user_data=db_user_model)
        return created_user

    async def get_user_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserModel]:
        return await self.user_repository.get_by_email(db, email=email)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[UserModel]:
        user = await self.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user