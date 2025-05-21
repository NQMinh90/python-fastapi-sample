from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session as SQLAlchemySession

from app.repositories.base_repository import BaseRepository

# Generic Types cho Service, liên kết với các type của Repository
RepoModelType = TypeVar("RepoModelType") # Kiểu model mà repository quản lý
RepoCreateSchemaType = TypeVar("RepoCreateSchemaType", bound=BaseModel) # Schema tạo của repo
RepoUpdateSchemaType = TypeVar("RepoUpdateSchemaType", bound=BaseModel) # Schema cập nhật của repo

# RepositoryType phải là một subclass của BaseRepository với các generic types tương ứng
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository[RepoModelType, RepoCreateSchemaType, RepoUpdateSchemaType])

class BaseService(Generic[RepositoryType, RepoModelType, RepoCreateSchemaType, RepoUpdateSchemaType]):
    """
    Lớp Service cơ sở, nhận một instance của Repository.
    Các phương thức ở đây thường gọi các phương thức tương ứng của repository.
    Business logic có thể được thêm vào đây.
    """
    def __init__(self, repository: RepositoryType):
        self.repository = repository

    async def get(self, db: SQLAlchemySession, id: Any) -> Optional[RepoModelType]:
        return await self.repository.get(db, id=id)

    async def get_multi(self, db: SQLAlchemySession, *, skip: int = 0, limit: int = 100) -> List[RepoModelType]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)

    async def create(self, db: SQLAlchemySession, *, obj_in: RepoCreateSchemaType) -> RepoModelType:
        # Thêm business logic ở đây nếu cần (trước hoặc sau khi gọi repo)
        return await self.repository.create(db, obj_in=obj_in)

    async def update(self, db: SQLAlchemySession, *, db_obj: RepoModelType, obj_in: RepoUpdateSchemaType | dict[str, Any]) -> RepoModelType:
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def delete(self, db: SQLAlchemySession, *, id: Any) -> Optional[RepoModelType]:
        return await self.repository.delete(db, id=id)