from fastapi import Depends

from app.api.base_api import BaseAPIRouter
from app.models.schemas import (
    JobPostTagSchema,
    JobPostTagCreate,
    JobPostTagUpdate,
    JobPostTagInDBBase
)
from app.services.impl.job_post_tag_service import JobPostTagService
from app.repositories.impl.job_post_tag_repository import JobPostTagRepository
from app.dependencies import get_db, get_current_active_user # <--- THAY ĐỔI IMPORT


# --- Dependencies cho JobPostTag ---

def get_job_post_tag_repository() -> JobPostTagRepository:
    return JobPostTagRepository()

def get_job_post_tag_service(repo: JobPostTagRepository = Depends(get_job_post_tag_repository)) -> JobPostTagService:
    return JobPostTagService(job_post_tag_repository=repo)

router = BaseAPIRouter[JobPostTagService, JobPostTagInDBBase, JobPostTagSchema, JobPostTagCreate, JobPostTagUpdate](
    service_dependency=get_job_post_tag_service,
    response_model_schema=JobPostTagSchema,
    create_model_schema=JobPostTagCreate,
    update_model_schema=JobPostTagUpdate,
    db_session_dependency=get_db,
    prefix="/job-post-tags",
    tags=["Job Post Tags"],
    dependencies=[Depends(get_current_active_user)] # Yêu cầu xác thực cho tất cả các route của JobPostTag
)