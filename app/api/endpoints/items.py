from fastapi import Depends
from app.api.base_api import BaseAPIRouter
from app.models.item import Item as ItemModel # Import SQLAlchemy model
from app.models.schemas import ItemSchema, ItemCreate, ItemUpdate
from app.services.impl.item_service import ItemService
from app.repositories.impl.item_repository import ItemRepository
from app.dependencies import get_db # <--- THAY ĐỔI IMPORT

def get_item_repository() -> ItemRepository:
    """Trả về một instance của ItemRepository (hiện tại là InMemory)."""
    return ItemRepository()

# Dependency cho ItemService
def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService:
    """Trả về một instance của ItemService với ItemRepository đã được inject."""
    return ItemService(item_repository=repo)

# Tạo router cho Items sử dụng BaseAPIRouter
router = BaseAPIRouter[ItemService, ItemModel, ItemSchema, ItemCreate, ItemUpdate](
    service_dependency=get_item_service,      # Dependency để lấy ItemService
    response_model_schema=ItemSchema,         # Schema cho response (GET, POST, PUT, DELETE)
    create_model_schema=ItemCreate,           # Schema cho request body khi tạo (POST)
    update_model_schema=ItemUpdate,           # Schema cho request body khi cập nhật (PUT)
    db_session_dependency=get_db,             # Dependency để lấy DB Session
    prefix="/items",
    tags=["Items"],
)