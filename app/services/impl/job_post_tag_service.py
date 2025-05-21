from app.services.base_service import BaseService
from app.repositories.impl.job_post_tag_repository import JobPostTagRepository
from app.models.schemas import JobPostTagInDBBase, JobPostTagCreate, JobPostTagUpdate

class JobPostTagService(BaseService[JobPostTagRepository, JobPostTagInDBBase, JobPostTagCreate, JobPostTagUpdate]):
    """
    Service cho JobPostTag.
    """
    def __init__(self, job_post_tag_repository: JobPostTagRepository):
        super().__init__(repository=job_post_tag_repository)
        # Thêm business logic cụ thể cho JobPostTag ở đây nếu cần