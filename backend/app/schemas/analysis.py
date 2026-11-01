from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    resume_id: int
    job_id: int


class SkillItem(BaseModel):
    name: str
    category: str
    aliases_matched: list[str] = Field(default_factory=list)
    priority: str | None = None
    weight: float | None = None


class RecommendationItem(BaseModel):
    skill: str
    category: str
    priority: str
    why_it_matters: str
    what_to_learn: str
    suggested_project: str
    next_steps: list[str]


class ScoreBreakdown(BaseModel):
    match_score: float
    skill_coverage: float
    weighted_skill_coverage: float
    text_similarity: float
    notes: list[str]


class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    resume_filename: str | None = None
    job_title: str | None = None
    job_company: str | None = None
    match_score: float
    skill_coverage: float
    weighted_skill_coverage: float
    text_similarity: float
    matched_skills: list
    missing_skills: list
    additional_skills: list
    recommendations: list
    score_notes: list[str] = Field(default_factory=list)
    category_breakdown: dict[str, dict[str, int]] = Field(default_factory=dict)
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisSummary(BaseModel):
    id: int
    resume_id: int
    job_id: int
    resume_filename: str | None = None
    job_title: str | None = None
    match_score: float
    skill_coverage: float
    created_at: datetime


class AnalysisListResponse(BaseModel):
    items: list[AnalysisSummary]
    total: int


class DashboardStats(BaseModel):
    resume_count: int
    job_count: int
    analysis_count: int
    average_match_score: float | None
    latest_analyses: list[AnalysisSummary]
