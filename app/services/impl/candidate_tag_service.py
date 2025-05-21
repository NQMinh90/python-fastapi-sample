from app.services.base_service import BaseService
from app.repositories.impl.candidate_tag_repository import CandidateTagRepository
from app.models.candidate_tag import CandidateTag as CandidateTagModel # Import SQLAlchemy model
from app.models.schemas import CandidateTagCreate, CandidateTagUpdate # Giữ Pydantic schemas

class CandidateTagService(BaseService[CandidateTagRepository, CandidateTagModel, CandidateTagCreate, CandidateTagUpdate]):
    """
    Service cho CandidateTag.
    """
    def __init__(self, repository: CandidateTagRepository):
        super().__init__(repository=repository)
        # Các phương thức của BaseService sẽ tự động hoạt động với CandidateTagModel.
        # FastAPI sẽ tự động chuyển đổi CandidateTagModel sang CandidateTagSchema (Pydantic)
        # khi trả về response nếu CandidateTagSchema có Config.from_attributes = True.