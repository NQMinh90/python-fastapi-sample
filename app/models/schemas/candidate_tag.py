from typing import Optional
from pydantic import BaseModel

# Schemas for CandidateTag
class CandidateTagBase(BaseModel):
    name: str
    description: Optional[str] = None

class CandidateTagCreate(CandidateTagBase):
    pass

class CandidateTagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CandidateTagInDBBase(CandidateTagBase):
    id: int

    class Config:
        from_attributes = True

class CandidateTagSchema(CandidateTagInDBBase):
    pass