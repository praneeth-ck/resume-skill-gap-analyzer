from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    company: str | None = Field(default=None, max_length=255)
    description: str = Field(min_length=20)


class JobResponse(BaseModel):
    id: int
    title: str
    company: str | None
    description: str
    required_skills: list
    created_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
