import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.database import get_db
from src.models import Resume, User
from src.schemas import ResumeCreate, ResumeResponse


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


@router.post("/{resume_id}/improve", response_model=ResumeResponse)
def improve_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.owner_id == current_user.id
    ).first()

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume writer. "
                    "Rewrite the user's resume text into a professional, "
                    "ATS-friendly resume summary. "
                    "Do NOT use placeholders like [Your Name]. "
                    "Do NOT create a template. "
                    "Use only the information provided by the user, "
                    "but improve wording, clarity, and professionalism."
                )
            },
            {
                "role": "user",
                "content": f"Improve this resume text:\n\n{resume.original_text}"
            }
        ],
        temperature=0.5
    )

    resume.improved_text = response.choices[0].message.content

    db.commit()
    db.refresh(resume)

    return resume