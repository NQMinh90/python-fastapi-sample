from app.services.base_service import BaseService
from app.repositories.impl.item_repository import ItemRepository
from app.models.schemas import ItemSchema, ItemCreate, ItemUpdate

class ItemService(BaseService[ItemRepository, ItemSchema, ItemCreate, ItemUpdate]):
    """
    ItemService cụ thể.
    Sử dụng ItemRepository và các schema tương ứng (ItemSchema, ItemCreate, ItemUpdate).
    """
    def __init__(self, item_repository: ItemRepository):
        super().__init__(repository=item_repository)
        # Có thể override các phương thức hoặc thêm business logic cụ thể cho Item ở đây