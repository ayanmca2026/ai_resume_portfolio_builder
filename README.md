# CAREER OS
## AI-Powered Resume, Portfolio & Career Intelligence Platform

## Features
- AI Resume Builder
- ATS Scanner
- Job Match Engine
- Career Twin
- Career Graph
- Skill Gap Analysis
- Career Roadmap
- AI Cover Letter
- Portfolio Builder
- AI Career Coach
- Interview Simulator
- Application Tracker
- Application Pack Generator
- PDF/DOCX Export
- Resume Import
- Gemini AI
- Mock AI
- Career Analytics

## Architecture
FastAPI, Python, Jinja2, HTMX, SQLAlchemy, Alembic, Gemini, SQLite/PostgreSQL, ReportLab, python-docx

## Installation
```bash
git clone https://github.com/ayanmca2026/ai_resume_portfolio_builder.git
cd ai_resume_portfolio_builder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## Environment Variables
- `APP_NAME`: Name of the application
- `APP_ENV`: Environment (development/production)
- `SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Connection string (SQLite/PostgreSQL)
- `AI_PROVIDER`: gemini or mock
- `GEMINI_API_KEY`: API key for Google Gemini

## Testing
```bash
pytest -q
```

## Docker
```bash
docker compose up --build
```

## Deployment
Render deployment is supported via `render.yaml`. It automatically provisions a PostgreSQL database and sets up the web service.

## Security
- JWT authentication
- HttpOnly, Secure cookies
- bcrypt password hashing
- Upload validation (MIME types, size limits)
- Secret management via environment variables

GitHub: https://github.com/ayanmca2026
