from app.services.base_service import BaseService
from app.repositories.impl.job_post_tag_repository import JobPostTagRepository
from app.models.job_post_tag import JobPostTag as JobPostTagModel # Import SQLAlchemy model
from app.models.schemas import JobPostTagCreate, JobPostTagUpdate # Giữ Pydantic schemas

class JobPostTagService(BaseService[JobPostTagRepository, JobPostTagModel, JobPostTagCreate, JobPostTagUpdate]):
    """
    Service cho JobPostTag.
    """
    def __init__(self, job_post_tag_repository: JobPostTagRepository):
        super().__init__(repository=job_post_tag_repository)
        # Các phương thức của BaseService sẽ tự động hoạt động với JobPostTagModel.
        # FastAPI sẽ tự động chuyển đổi JobPostTagModel sang JobPostTagSchema (Pydantic)
        # khi trả về response nếu JobPostTagSchema có Config.from_attributes = True.