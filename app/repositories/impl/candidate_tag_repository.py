from app.models.schemas import CandidateTagCreate, CandidateTagUpdate, CandidateTagInDBBase
from app.repositories.in_memory_repository import InMemoryRepository

class CandidateTagRepository(InMemoryRepository[CandidateTagInDBBase, CandidateTagCreate, CandidateTagUpdate]):
    """
    Repository cho CandidateTag, sử dụng InMemoryRepository.
    """
    def __init__(self):
        super().__init__(model_schema=CandidateTagInDBBase)