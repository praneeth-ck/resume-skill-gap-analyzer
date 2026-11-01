from datetime import datetime

from pydantic import BaseModel, Field


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    extracted_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeSummary(BaseModel):
    id: int
    filename: str
    file_type: str
    text_preview: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    items: list[ResumeSummary]
    total: int


class TextPreview(BaseModel):
    preview: str = Field(default="")
