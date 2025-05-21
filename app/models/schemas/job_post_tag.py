from typing import Optional
from pydantic import BaseModel

# Schemas for JobPostTag
class JobPostTagBase(BaseModel):
    name: str
    description: Optional[str] = None

class JobPostTagCreate(JobPostTagBase):
    pass

class JobPostTagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class JobPostTagInDBBase(JobPostTagBase):
    id: int

    class Config:
        from_attributes = True

class JobPostTagSchema(JobPostTagInDBBase):
    pass