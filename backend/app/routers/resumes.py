from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeListResponse, ResumeResponse, ResumeSummary
from app.services.resume_parser import extract_resume_text
from app.utils.file_validation import validate_and_read_upload

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


def _owned_resume(db: Session, current_user: User, resume_id: int) -> Resume:
    resume = db.get(Resume, resume_id)
    if resume is None or resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    return resume


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Resume:
    data, original_name, file_type = await validate_and_read_upload(file)
    extracted = extract_resume_text(data, file_type)

    settings = get_settings()
    stored_name = f"{uuid4().hex}{Path(original_name).suffix.lower()}"
    destination = settings.upload_path / stored_name
    destination.write_bytes(data)

    resume = Resume(
        user_id=current_user.id,
        filename=original_name,
        file_type=file_type,
        file_path=str(destination),
        extracted_text=extracted,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("", response_model=ResumeListResponse)
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeListResponse:
    resumes = db.scalars(
        select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc())
    ).all()
    items = [
        ResumeSummary(
            id=resume.id,
            filename=resume.filename,
            file_type=resume.file_type,
            text_preview=resume.extracted_text[:400],
            created_at=resume.created_at,
        )
        for resume in resumes
    ]
    return ResumeListResponse(items=items, total=len(items))


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Resume:
    return _owned_resume(db, current_user, resume_id)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    resume = _owned_resume(db, current_user, resume_id)
    path = Path(resume.file_path)
    db.delete(resume)
    db.commit()
    if path.exists():
        path.unlink(missing_ok=True)
