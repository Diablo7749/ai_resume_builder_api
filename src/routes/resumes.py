from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.database import get_db
from src.models import Resume, User
from src.schemas import ResumeCreate, ResumeResponse


router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/", response_model=ResumeResponse)
def create_resume(
    resume_data: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_resume = Resume(
        title=resume_data.title,
        original_text=resume_data.original_text,
        improved_text=None,
        owner_id=current_user.id
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume


@router.get("/", response_model=list[ResumeResponse])
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = db.query(Resume).filter(
        Resume.owner_id == current_user.id
    ).all()

    return resumes