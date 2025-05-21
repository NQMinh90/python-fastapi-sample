from typing import Any, Generic, List, Optional, Dict, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession # <--- THAY ĐỔI
from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete

from app.db.base_class import Base # Giả sử Base là declarative_base của bạn
from app.repositories.base_repository import BaseRepository, CreateSchemaType, UpdateSchemaType

# ModelType ở đây sẽ là một class SQLAlchemy model (kế thừa từ Base)
SQLAlchemyModelType = TypeVar("SQLAlchemyModelType", bound=Base)

class SQLAlchemyRepository(
    BaseRepository[SQLAlchemyModelType, CreateSchemaType, UpdateSchemaType],
    Generic[SQLAlchemyModelType, CreateSchemaType, UpdateSchemaType]
):
    """
    Một Repository cơ sở sử dụng SQLAlchemy để tương tác với cơ sở dữ liệu.
    SQLAlchemyModelType là class model SQLAlchemy (ví dụ: User, Item).
    """
    def __init__(self, model: Type[SQLAlchemyModelType]):
        """
        Khởi tạo repository với một model SQLAlchemy cụ thể.
        :param model: Class model SQLAlchemy.
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[SQLAlchemyModelType]:
        """
        Lấy một đối tượng theo ID.
        """
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[SQLAlchemyModelType]:
        """
        Lấy nhiều đối tượng, có hỗ trợ phân trang.
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> SQLAlchemyModelType:
        """
        Tạo một đối tượng mới.
        obj_in là một Pydantic schema.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # Tạo instance của SQLAlchemy model
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: SQLAlchemyModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> SQLAlchemyModelType:
        """
        Cập nhật một đối tượng đã có trong DB.
        db_obj là instance SQLAlchemy model hiện tại.
        obj_in có thể là Pydantic schema hoặc một dict.
        """
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> Optional[SQLAlchemyModelType]:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj