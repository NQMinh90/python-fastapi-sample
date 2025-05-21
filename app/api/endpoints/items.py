from fastapi import Depends
from sqlalchemy.orm import Session as SQLAlchemySession

from app.api.base_api import BaseAPIRouter
from app.models.schemas import ItemSchema, ItemCreate, ItemUpdate
from app.services.impl.item_service import ItemService
from app.repositories.impl.item_repository import ItemRepository
from app.db.session import get_db

# --- Dependencies cho Item ---

# Dependency cho ItemRepository
# Nếu ItemRepository của bạn cần db (ví dụ: SQLAlchemyRepository), bạn sẽ inject db ở đây.
# def get_item_repository(db: SQLAlchemySession = Depends(get_db)) -> ItemRepository:
# return ItemRepository(db=db) # Ví dụ nếu repo cần db session

def get_item_repository() -> ItemRepository:
    """Trả về một instance của ItemRepository (hiện tại là InMemory)."""
    return ItemRepository()

# Dependency cho ItemService
def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService:
    """Trả về một instance của ItemService với ItemRepository đã được inject."""
    return ItemService(item_repository=repo)

# Tạo router cho Items sử dụng BaseAPIRouter
router = BaseAPIRouter[ItemService, ItemSchema, ItemSchema, ItemCreate, ItemUpdate](
    service_dependency=get_item_service,      # Dependency để lấy ItemService
    response_model_schema=ItemSchema,         # Schema cho response (GET, POST, PUT, DELETE)
    create_model_schema=ItemCreate,           # Schema cho request body khi tạo (POST)
    update_model_schema=ItemUpdate,           # Schema cho request body khi cập nhật (PUT)
    db_session_dependency=get_db,             # Dependency để lấy DB Session
    prefix="/items",
    tags=["Items"],
)