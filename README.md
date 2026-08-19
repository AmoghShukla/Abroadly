# Abroadly

An evidence-led Master's-abroad planning platform for Germany and Australia. It will recommend specific programs based on a student's profile, explain deterministic eligibility and budget fit, and retain source provenance for every requirement, cost, and deadline.

## Working MVP included

- FastAPI app with versioned `GET /api/v1/health`
- PostgreSQL-ready SQLAlchemy 2.0 session and Alembic configuration
- Docker Compose for API, PostgreSQL, Redis, and frontend
- React/Vite Material UI profile-to-recommendations experience (no Tailwind)
- Environment-based configuration and request ID middleware
- Deterministic programme-level eligibility, profile-match and budget-fit scoring
- A Germany/Australia programme catalogue with official-source links and last-verified labels
- Safe what-if simulation and an API advisor action list
- Password-hashed account registration/login with expiring bearer tokens
- Protected user profile, shortlist, application and document endpoints
- Resume upload with explicitly review-required draft extraction
- Dashboard navigation, country selection, document vault, applications, About page, and light/dark mode

All catalogue results are explicitly **SEED / DEMO DATA**. They are included so the full recommendation workflow is testable, not as a claim that requirements or costs are production-verified. The UI prominently asks students to verify official programme pages.

## Run

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Frontend: `http://localhost:5173`  
API docs: `http://localhost:8000/docs`  
Health: `http://localhost:8000/api/v1/health`

## Product constraints

LLMs will only explain structured facts or analyse student-provided material. They will not create official requirements, tuition, deadlines, or admissions claims. Database-backed facts will retain source URL and verification-date provenance.

## API endpoints

- `GET /api/v1/programs` and `GET /api/v1/programs/{id}`
- `POST /api/v1/auth/register` and `POST /api/v1/auth/login`
- `GET|PUT /api/v1/profile`
- `POST /api/v1/recommendations`, `GET /api/v1/recommendations/top10`
- `POST /api/v1/simulation`
- `GET|POST /api/v1/shortlist`
- `POST /api/v1/ai/advisor`

## Before production

Replace the in-memory demo store with the normalized SQLAlchemy domain models, run reviewed Alembic migrations, add JWT/RBAC and document storage, and build verified ingestion adapters for DAAD and official university sources. Those steps are required before presenting any academic requirement as authoritative.
