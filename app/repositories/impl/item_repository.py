from app.models.schemas import ItemSchema, ItemCreate, ItemUpdate
from app.repositories.in_memory_repository import InMemoryRepository

class ItemRepository(InMemoryRepository[ItemSchema, ItemCreate, ItemUpdate]):
    """
    ItemRepository cụ thể, sử dụng InMemoryRepository.
    ItemSchema sẽ đóng vai trò là "ModelType" được lưu trữ trong InMemoryRepository.
    """
    def __init__(self):
        super().__init__(model_schema=ItemSchema) # ItemSchema là Pydantic model cho item