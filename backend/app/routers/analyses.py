from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.analysis import Analysis
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisListResponse,
    AnalysisResponse,
    AnalysisSummary,
    DashboardStats,
)
from app.services.recommendation import generate_recommendations
from app.services.similarity import (
    compute_overall_score,
    compute_skill_coverage,
    compute_text_similarity,
    compute_weighted_skill_coverage,
)
from app.services.skill_matcher import category_breakdown, compare_skills

router = APIRouter(prefix="/api/analyses", tags=["analyses"])


def _owned_analysis(db: Session, current_user: User, analysis_id: int) -> Analysis:
    analysis = db.get(Analysis, analysis_id)
    if analysis is None or analysis.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found.")
    return analysis


def _to_response(analysis: Analysis) -> AnalysisResponse:
    matched = analysis.matched_skills or []
    missing = analysis.missing_skills or []
    additional = analysis.additional_skills or []
    return AnalysisResponse(
        id=analysis.id,
        resume_id=analysis.resume_id,
        job_id=analysis.job_id,
        resume_filename=analysis.resume.filename if analysis.resume else None,
        job_title=analysis.job.title if analysis.job else None,
        job_company=analysis.job.company if analysis.job else None,
        match_score=analysis.match_score,
        skill_coverage=analysis.skill_coverage,
        weighted_skill_coverage=analysis.weighted_skill_coverage,
        text_similarity=analysis.text_similarity,
        matched_skills=matched,
        missing_skills=missing,
        additional_skills=additional,
        recommendations=analysis.recommendations or [],
        category_breakdown=category_breakdown(matched, missing, additional),
        created_at=analysis.created_at,
    )


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(
    payload: AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalysisResponse:
    resume = db.get(Resume, payload.resume_id)
    job = db.get(Job, payload.job_id)
    if resume is None or resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")

    comparison = compare_skills(resume.extracted_text, job.description)
    matched = comparison["matched_skills"]
    missing = comparison["missing_skills"]
    additional = comparison["additional_skills"]

    notes: list[str] = []
    coverage, note = compute_skill_coverage(len(matched), len(matched) + len(missing))
    if note:
        notes.append(note)
    weighted, note = compute_weighted_skill_coverage(matched, missing)
    if note:
        notes.append(note)
    similarity, note = compute_text_similarity(resume.extracted_text, job.description)
    if note:
        notes.append(note)
    overall = compute_overall_score(weighted, similarity, notes)
    recommendations = generate_recommendations(missing, job.title)

    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        match_score=overall,
        skill_coverage=coverage,
        weighted_skill_coverage=weighted,
        text_similarity=similarity,
        matched_skills=matched,
        missing_skills=missing,
        additional_skills=additional,
        recommendations=recommendations,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    response = _to_response(analysis)
    response.score_notes = notes
    return response


@router.get("", response_model=AnalysisListResponse)
def list_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalysisListResponse:
    analyses = db.scalars(
        select(Analysis).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc())
    ).all()
    items = [
        AnalysisSummary(
            id=item.id,
            resume_id=item.resume_id,
            job_id=item.job_id,
            resume_filename=item.resume.filename if item.resume else None,
            job_title=item.job.title if item.job else None,
            match_score=item.match_score,
            skill_coverage=item.skill_coverage,
            created_at=item.created_at,
        )
        for item in analyses
    ]
    return AnalysisListResponse(items=items, total=len(items))


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardStats:
    resume_count = db.scalar(select(func.count(Resume.id)).where(Resume.user_id == current_user.id)) or 0
    job_count = db.scalar(select(func.count(Job.id)).where(Job.user_id == current_user.id)) or 0
    analysis_count = db.scalar(select(func.count(Analysis.id)).where(Analysis.user_id == current_user.id)) or 0
    average = db.scalar(select(func.avg(Analysis.match_score)).where(Analysis.user_id == current_user.id))
    latest = db.scalars(
        select(Analysis).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).limit(5)
    ).all()
    return DashboardStats(
        resume_count=resume_count,
        job_count=job_count,
        analysis_count=analysis_count,
        average_match_score=round(float(average), 2) if average is not None else None,
        latest_analyses=[
            AnalysisSummary(
                id=item.id,
                resume_id=item.resume_id,
                job_id=item.job_id,
                resume_filename=item.resume.filename if item.resume else None,
                job_title=item.job.title if item.job else None,
                match_score=item.match_score,
                skill_coverage=item.skill_coverage,
                created_at=item.created_at,
            )
            for item in latest
        ],
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalysisResponse:
    return _to_response(_owned_analysis(db, current_user, analysis_id))


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    analysis = _owned_analysis(db, current_user, analysis_id)
    db.delete(analysis)
    db.commit()
