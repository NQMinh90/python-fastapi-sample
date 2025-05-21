from fastapi import Depends

from app.api.base_api import BaseAPIRouter
from app.models.schemas import (
    CandidateTagSchema,
    CandidateTagCreate,
    CandidateTagUpdate,
    CandidateTagInDBBase
)
from app.services.impl.candidate_tag_service import CandidateTagService
from app.repositories.impl.candidate_tag_repository import CandidateTagRepository
from app.db.session import get_db
from app.api.dependencies import get_current_active_user # Bảo vệ endpoint

# --- Dependencies cho CandidateTag ---

def get_candidate_tag_repository() -> CandidateTagRepository:
    return CandidateTagRepository()

def get_candidate_tag_service(repo: CandidateTagRepository = Depends(get_candidate_tag_repository)) -> CandidateTagService:
    return CandidateTagService(candidate_tag_repository=repo)

router = BaseAPIRouter[CandidateTagService, CandidateTagInDBBase, CandidateTagSchema, CandidateTagCreate, CandidateTagUpdate](
    service_dependency=get_candidate_tag_service,
    response_model_schema=CandidateTagSchema,
    create_model_schema=CandidateTagCreate,
    update_model_schema=CandidateTagUpdate,
    db_session_dependency=get_db,
    prefix="/candidate-tags",
    tags=["Candidate Tags"],
    dependencies=[Depends(get_current_active_user)] # Yêu cầu xác thực cho tất cả các route của CandidateTag
)