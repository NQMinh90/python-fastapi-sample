from app.models.item import Item as ItemModel # Import SQLAlchemy model cho Item
from app.models.schemas import ItemCreate, ItemUpdate # Giữ lại Pydantic schemas
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository

class ItemRepository(SQLAlchemyRepository[ItemModel, ItemCreate, ItemUpdate]):
    """
    ItemRepository cụ thể, sử dụng SQLAlchemyRepository để tương tác với DB.
    ItemModel là SQLAlchemy model.
    """
    def __init__(self):
        super().__init__(model=ItemModel) # Truyền class ItemModel SQLAlchemy