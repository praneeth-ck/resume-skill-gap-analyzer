# Resume Skill Gap Analyzer

A full-stack application that compares a resume with a job description, extracts skills with NLP, and shows matching skills, missing skills, additional skills, transparent match metrics, and learning recommendations.

This is not a hiring predictor. A missing skill means it was **not detected** in the uploaded resume, not that the candidate definitely lacks it.

## Features

- User registration, login, JWT authentication, and account-scoped data
- PDF and DOCX resume upload, validation, and text extraction
- Saved job descriptions with extracted required skills
- spaCy PhraseMatcher plus a curated skill dictionary with aliases
- Skill coverage, weighted coverage (mandatory vs preferred), and TF-IDF cosine similarity
- Rule-based recommendations that never tell users to claim unearned skills
- Interactive dashboard with Chart.js visualizations
- Analysis history, comparison, and deletion

## Technology stack

- **Frontend:** React, Vite, Axios, React Router, Chart.js, Lucide React
- **Backend:** FastAPI, SQLAlchemy, Pydantic, Uvicorn, JWT, Argon2
- **Database:** PostgreSQL with Alembic migrations
- **NLP:** spaCy, scikit-learn, PyMuPDF, python-docx

## Project structure

```
backend/
  app/                 FastAPI app, models, routers, NLP services
  alembic/             Database migrations
  tests/               pytest coverage
  uploads/             Private stored resumes (not publicly served)
frontend/              React application
docker-compose.yml     Local PostgreSQL
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or Docker)
- About 5 minutes for the spaCy English model download

## Installation

### 1. PostgreSQL

With Docker:

```bash
docker compose up -d db
```

Without Docker, create a database named `resume_analyzer` and a user that can access it.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
copy .env.example .env
```

On macOS/Linux, replace the activate line with `source .venv/bin/activate` and `cp .env.example .env`.

Edit `.env` if your PostgreSQL credentials differ:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/resume_analyzer
SECRET_KEY=replace-with-a-long-random-value
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Apply migrations (or let the API create tables on startup):

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive API.

### 3. Frontend

```bash
cd frontend
copy .env.example .env
npm install
npm run dev
```

Open http://localhost:5173.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | JWT signing key |
| `DATABASE_URL` | SQLAlchemy database URL |
| `CORS_ORIGINS` | Allowed frontend origins |
| `UPLOAD_DIR` | Private resume storage |
| `MAX_UPLOAD_BYTES` | Upload size cap (default 5 MB) |
| `SPACY_MODEL` | spaCy model name |
| `VITE_API_URL` | Frontend API base URL |

Never commit a real `.env` file.

## Typical workflow

1. Register or log in.
2. Upload a PDF or DOCX resume and review extracted text.
3. Save a job description.
4. Run analysis.
5. Review scores, skill lists, charts, and recommendations.
6. Reopen or compare past analyses from history.

## API documentation

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Sign in |
| GET | `/api/auth/me` | Current user |
| POST | `/api/resumes/upload` | Upload resume |
| GET | `/api/resumes` | List own resumes |
| GET | `/api/resumes/{id}` | Resume detail |
| DELETE | `/api/resumes/{id}` | Delete resume |
| POST | `/api/jobs` | Save job description |
| GET | `/api/jobs` | List jobs |
| GET | `/api/jobs/{id}` | Job detail |
| DELETE | `/api/jobs/{id}` | Delete job |
| POST | `/api/analyses` | Run analysis |
| GET | `/api/analyses` | History |
| GET | `/api/analyses/dashboard` | Dashboard stats |
| GET | `/api/analyses/{id}` | Analysis detail |
| DELETE | `/api/analyses/{id}` | Delete analysis |

All resume, job, and analysis routes require `Authorization: Bearer <token>` and only return the current user's records.

## Scoring

- **Skill coverage:** matching skills / required skills
- **Weighted skill coverage:** mandatory skills weigh more than preferred skills
- **Text similarity:** TF-IDF + cosine similarity
- **Overall estimate:** `0.7 * weighted coverage + 0.3 * text similarity`

If no job skills are detected, coverage metrics stay at 0 with an explanation instead of a misleading 100%.

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm test
```

## Security notes

- Passwords are hashed with Argon2.
- Uploaded files are validated by extension and magic bytes, stored under UUID names, and never served as public URLs.
- File names from users are not trusted as paths.
- Resume text is not written to application logs.

## Limitations

- Skill extraction uses a curated dictionary. Domain-specific or uncommon skills may be missed.
- Recommendations are rule-based templates, not a generative model.
- OCR is not included; scanned image-only PDFs will be rejected if no text is found.
