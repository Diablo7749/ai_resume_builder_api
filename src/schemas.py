from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ResumeCreate(BaseModel):
    title: str
    original_text: str


class ResumeResponse(BaseModel):
    id: int
    title: str
    original_text: str
    improved_text: str | None

    class Config:
        from_attributes = True