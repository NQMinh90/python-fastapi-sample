from typing import Optional
from sqlalchemy.orm import Session as SQLAlchemySession # Giữ để nhất quán

from app.models.schemas import UserCreate, UserUpdate, UserInDBBase as UserInDB # Sử dụng UserInDB để lưu trữ
from app.repositories.in_memory_repository import InMemoryRepository
from app.core.security import get_password_hash

# Trong ví dụ này, UserSchema được dùng làm "model" lưu trữ trong InMemoryRepository.
# Điều này có nghĩa là chúng ta sẽ lưu trữ đối tượng UserSchema (bao gồm cả hashed_password nếu có).
# Để an toàn hơn, chúng ta nên tạo một UserInDB schema riêng để lưu trữ,
# nhưng để đơn giản hóa với InMemoryRepository, chúng ta sẽ điều chỉnh logic create.

class UserRepository(InMemoryRepository[UserInDB, UserCreate, UserUpdate]):
    """
    UserRepository cụ thể, sử dụng InMemoryRepository.
    UserInDB sẽ đóng vai trò là "ModelType" được lưu trữ trong InMemoryRepository.
    """
    def __init__(self):
        super().__init__(model_schema=UserInDB) # UserInDB là Pydantic model để lưu trữ user

    async def get_by_email(self, db: SQLAlchemySession, *, email: str) -> Optional[UserInDB]:
        # db không dùng ở đây nhưng giữ để nhất quán
        for user in self._data.values():
            if user.email == email:
                return user
        return None

    # Ghi đè phương thức create để hash password (nếu dùng UserSchema trực tiếp để lưu)
    # Tuy nhiên, tốt hơn là Service sẽ xử lý việc hash password trước khi gọi repo.
    # Vì vậy, chúng ta sẽ để Service làm việc đó.