from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobListResponse, JobResponse
from app.services.skill_extractor import extract_skills

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def _owned_job(db: Session, current_user: User, job_id: int) -> Job:
    job = db.get(Job, job_id)
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found.")
    return job


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Job:
    skills = extract_skills(payload.description)
    job = Job(
        user_id=current_user.id,
        title=payload.title.strip(),
        company=payload.company.strip() if payload.company else None,
        description=payload.description.strip(),
        required_skills=skills,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=JobListResponse)
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobListResponse:
    jobs = db.scalars(select(Job).where(Job.user_id == current_user.id).order_by(Job.created_at.desc())).all()
    return JobListResponse(items=list(jobs), total=len(jobs))


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Job:
    return _owned_job(db, current_user, job_id)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    job = _owned_job(db, current_user, job_id)
    db.delete(job)
    db.commit()
