from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession # Sử dụng AsyncSession
from sqlalchemy import select
from app.models.user import User as UserModel # Import SQLAlchemy model cho User
from app.models.schemas import UserCreate, UserUpdate, UserInDBBase as UserInDB # Giữ Pydantic schemas
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.core.security import get_password_hash

# Trong ví dụ này, UserSchema được dùng làm "model" lưu trữ trong InMemoryRepository.
# Điều này có nghĩa là chúng ta sẽ lưu trữ đối tượng UserSchema (bao gồm cả hashed_password nếu có).
# Để an toàn hơn, chúng ta nên tạo một UserInDB schema riêng để lưu trữ,
# nhưng để đơn giản hóa với InMemoryRepository, chúng ta sẽ điều chỉnh logic create.

class UserRepository(SQLAlchemyRepository[UserModel, UserCreate, UserUpdate]):
    """
    UserRepository cụ thể, sử dụng SQLAlchemyRepository để tương tác với DB.
    UserModel là SQLAlchemy model.
    """
    def __init__(self):
        super().__init__(model=UserModel) # UserInDB là Pydantic model để lưu trữ user

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserModel]:
        """
        Lấy một user theo email.
        """
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create_db_user_with_hashed_password(self, db: AsyncSession, *, user_data: UserModel) -> UserModel:
        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)
        return user_data

    # Các phương thức CRUD cơ bản (get, get_multi, create, update, delete)
    # đã được cung cấp bởi SQLAlchemyRepository.
    # Bạn có thể override chúng ở đây nếu cần logic đặc biệt cho User.
    
    # async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> UserModel:
    #     """
    #     Override phương thức create để xử lý việc băm mật khẩu.
    #     obj_in ở đây là UserCreate.
    #     """
    #     hashed_password = get_password_hash(obj_in.password)
    #     db_obj = self.model(
    #         email=obj_in.email,
    #         full_name=obj_in.full_name, # Giả sử UserCreate có full_name
    #         hashed_password=hashed_password,
    #         is_active=obj_in.is_active if hasattr(obj_in, 'is_active') else True,
    #         is_superuser=obj_in.is_superuser if hasattr(obj_in, 'is_superuser') else False
    #     )
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj