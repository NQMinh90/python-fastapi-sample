from app.models.schemas import JobPostTagCreate, JobPostTagUpdate, JobPostTagInDBBase
from app.repositories.in_memory_repository import InMemoryRepository

class JobPostTagRepository(InMemoryRepository[JobPostTagInDBBase, JobPostTagCreate, JobPostTagUpdate]):
    """
    Repository cho JobPostTag, sử dụng InMemoryRepository.
    """
    def __init__(self):
        super().__init__(model_schema=JobPostTagInDBBase)