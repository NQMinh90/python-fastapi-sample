from app.services.base_service import BaseService
from app.repositories.impl.candidate_tag_repository import CandidateTagRepository
from app.models.schemas import CandidateTagInDBBase, CandidateTagCreate, CandidateTagUpdate

class CandidateTagService(BaseService[CandidateTagRepository, CandidateTagInDBBase, CandidateTagCreate, CandidateTagUpdate]):
    """
    Service cho CandidateTag.
    """
    def __init__(self, candidate_tag_repository: CandidateTagRepository):
        super().__init__(repository=candidate_tag_repository)
        # Thêm business logic cụ thể cho CandidateTag ở đây nếu cần