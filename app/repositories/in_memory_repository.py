from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session as SQLAlchemySession # Giữ để nhất quán interface

from app.repositories.base_repository import BaseRepository, CreateSchemaType, UpdateSchemaType

# Mock ModelType cho lưu trữ in-memory, thường là Pydantic schema
InMemoryModelType = TypeVar("InMemoryModelType", bound=BaseModel) # Model lưu trữ sẽ là Pydantic model

class InMemoryRepository(
    BaseRepository[InMemoryModelType, CreateSchemaType, UpdateSchemaType],
    Generic[InMemoryModelType, CreateSchemaType, UpdateSchemaType]
):
    """
    Một Repository cơ sở sử dụng danh sách trong bộ nhớ để lưu trữ dữ liệu.
    Hữu ích cho việc thử nghiệm hoặc các ứng dụng đơn giản.
    InMemoryModelType là Pydantic schema được sử dụng để đại diện cho "bản ghi" trong bộ nhớ.
    """
    def __init__(self, model_schema: Type[InMemoryModelType]):
        self.model_schema = model_schema # Pydantic schema dùng để lưu trữ (ví dụ ItemSchema)
        self._data: Dict[int, InMemoryModelType] = {}
        self._current_id: int = 0

    async def get(self, db: SQLAlchemySession, id: Any) -> Optional[InMemoryModelType]:
        # db không được sử dụng ở đây nhưng giữ để nhất quán interface
        return self._data.get(int(id))

    async def get_multi(
        self, db: SQLAlchemySession, *, skip: int = 0, limit: int = 100
    ) -> List[InMemoryModelType]:
        items = list(self._data.values())
        return items[skip : skip + limit]

    async def create(self, db: SQLAlchemySession, *, obj_in: CreateSchemaType) -> InMemoryModelType:
        self._current_id += 1
        item_data = obj_in.model_dump()
        item_data["id"] = self._current_id # Gán ID mới
        new_item = self.model_schema(**item_data) # Tạo instance của model_schema (ví dụ ItemSchema)
        self._data[self._current_id] = new_item
        return new_item

    async def update(
        self, db: SQLAlchemySession, *, db_obj: InMemoryModelType, obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> InMemoryModelType:
        update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        updated_item = db_obj.model_copy(update=update_data) # Sử dụng model_copy cho Pydantic v2
        self._data[db_obj.id] = updated_item
        return updated_item

    async def delete(self, db: SQLAlchemySession, *, id: Any) -> Optional[InMemoryModelType]:
        item_id = int(id)
        return self._data.pop(item_id, None)