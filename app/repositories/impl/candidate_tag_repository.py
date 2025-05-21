from app.models.candidate_tag import CandidateTag as CandidateTagModel # Import SQLAlchemy model
from app.models.schemas import CandidateTagCreate, CandidateTagUpdate # Giữ lại Pydantic schemas
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository

class CandidateTagRepository(SQLAlchemyRepository[CandidateTagModel, CandidateTagCreate, CandidateTagUpdate]):
    """
    Repository cho CandidateTag, sử dụng InMemoryRepository.
    """
    def __init__(self):
        super().__init__(model=CandidateTagModel)

# Bạn có thể thêm các phương thức tùy chỉnh cho CandidateTag ở đây nếu cần,
# ví dụ: get_by_name, v.v.