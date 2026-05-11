# AI Resume Builder API

AI-powered REST API for creating, managing, and improving resumes using FastAPI and OpenAI.

## Features

- User registration
- User authentication (JWT)
- Protected API endpoints
- Create resumes
- View user-specific resumes
- AI-powered resume improvement
- OpenAI API integration
- SQLite database
- SQLAlchemy ORM
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- OpenAI API
- Pydantic
- Uvicorn
- python-dotenv

## Project Structure

```text
ai_resume_builder_api/
│
├── src/
│   ├── routes/
│   │   ├── users.py
│   │   └── resumes.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── resume_builder.db
