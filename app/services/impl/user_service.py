from typing import Optional, Any
from sqlalchemy.orm import Session as SQLAlchemySession

from app.core.security import get_password_hash, verify_password
from app.models.schemas import UserCreate, UserUpdate, UserInDBBase as UserInDB # Service làm việc với UserInDB
from app.repositories.impl.user_repository import UserRepository
from app.services.base_service import BaseService

class UserService(BaseService[UserRepository, UserInDB, UserCreate, UserUpdate]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(repository=user_repository)
        self.user_repository = user_repository # Gán lại để có type hinting tốt hơn

    async def create_user(self, db: SQLAlchemySession, *, obj_in: UserCreate) -> UserInDB:
        hashed_password = get_password_hash(obj_in.password)
        # Tạo một dict từ UserCreate, sau đó cập nhật password và loại bỏ password gốc
        user_data_for_db = obj_in.model_dump(exclude={"password"})
        user_data_for_db["hashed_password"] = hashed_password

        # InMemoryRepository.create mong đợi một CreateSchemaType,
        # nhưng chúng ta đã xử lý password, nên cần tạo UserInDB object trực tiếp
        # hoặc điều chỉnh BaseRepository/InMemoryRepository để chấp nhận dict.
        # Hiện tại, InMemoryRepository.create nhận CreateSchemaType, rồi model_dump() nó.
        # Chúng ta sẽ tạo một đối tượng UserInDB tạm thời để truyền vào.
        # Hoặc, tốt hơn là UserRepository nên có một phương thức create_with_hashed_password.
        # Để đơn giản, chúng ta sẽ truyền một đối tượng UserCreate đã được sửa đổi.

        # Cách tiếp cận tốt hơn: BaseRepository.create nên nhận obj_in là CreateSchemaType
        # và UserRepository.create sẽ xử lý việc tạo UserInDB từ UserCreate.
        # Tuy nhiên, để giữ BaseRepository chung chung, Service sẽ chuẩn bị dữ liệu.

        db_user = UserInDB(**user_data_for_db, id=0) # id sẽ được gán bởi InMemoryRepo
        return await self.user_repository.create(db, obj_in=db_user) # Truyền UserInDB

    async def get_user_by_email(self, db: SQLAlchemySession, *, email: str) -> Optional[UserInDB]:
        return await self.user_repository.get_by_email(db, email=email)

    async def authenticate(self, db: SQLAlchemySession, *, email: str, password: str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user