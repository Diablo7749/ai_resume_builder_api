from fastapi import FastAPI

from src.database import Base, engine
from src.routes import users, resumes


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Builder API",
    description="API for creating and improving resumes",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(resumes.router)


@app.get("/")
def root():
    return {"message": "AI Resume Builder API is running"}