from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session as SQLAlchemySession

# Generic Types
ModelType = TypeVar("ModelType")  # Đại diện cho ORM model instance (ví dụ: SQLAlchemy model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel) # Pydantic schema cho việc tạo mới
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) # Pydantic schema cho việc cập nhật

class BaseRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Lớp Repository cơ sở trừu tượng cho các thao tác CRUD.
    ModelType là kiểu của ORM model (ví dụ: một class SQLAlchemy).
    """
    # def __init__(self, model: Type[ModelType]):
    #     """Trong một SQLAlchemy setup thực tế, model sẽ là class SQLAlchemy model."""
    #     self.model = model

    @abstractmethod
    async def get(self, db: SQLAlchemySession, id: Any) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def get_multi(self, db: SQLAlchemySession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        pass

    @abstractmethod
    async def create(self, db: SQLAlchemySession, *, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    async def update(self, db: SQLAlchemySession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        pass

    @abstractmethod
    async def delete(self, db: SQLAlchemySession, *, id: Any) -> Optional[ModelType]:
        pass