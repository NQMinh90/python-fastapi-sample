from app.models.job_post_tag import JobPostTag as JobPostTagModel # Import SQLAlchemy model
from app.models.schemas import JobPostTagCreate, JobPostTagUpdate # Giữ lại Pydantic schemas
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository

class JobPostTagRepository(SQLAlchemyRepository[JobPostTagModel, JobPostTagCreate, JobPostTagUpdate]):
    """
    Repository cho JobPostTag, sử dụng SQLAlchemyRepository để tương tác với DB.
    JobPostTagModel là SQLAlchemy model.
    """
    def __init__(self):
        super().__init__(model=JobPostTagModel) # Truyền class JobPostTagModel SQLAlchemy
        # Bạn có thể thêm các phương thức tùy chỉnh cho JobPostTag ở đây nếu cần,
        # ví dụ: get_by_name, v.v.