# Abroadly

> Your evidence-led command centre for planning a Master's degree abroad.

**Abroadly** helps students turn an academic profile into a practical application plan. It recommends individual Master's programmes—not generic university lists—then shows eligibility signals, estimated affordability, source links, and the next actions to take.

The MVP currently supports **Germany** and **Australia** and is designed to expand to additional countries without rewriting the recommendation core.

> “To be Ballin, You got to Be-All-In” — Amogh Shukla

## Why Abroadly?

Planning to study abroad is often fragmented: programme research lives in browser tabs, costs live in spreadsheets, and deadlines get lost in notes. Abroadly brings the high-signal decisions together while keeping a clear boundary between sourced facts and AI-assisted guidance.

- 🎯 **Programme-level recommendations** tailored to the student's profile
- ✅ **Deterministic eligibility**—never framed as an admission probability
- 💰 **Budget-aware matching** with estimated total cost comparison
- 🔎 **Source provenance** through official links and verification labels
- 📄 **Resume upload** with review-required extraction
- 🧭 **One dashboard** for profile, discovery, documents, and applications

## Features

### Student experience

- Secure account registration and sign-in
- Profile onboarding for academic history, CGPA, budget, test scores, and target country
- Country selection for Germany, Australia, or both
- Personalised Top Programme Matches
- Dark and light themes
- Responsive navigation across Dashboard, Discover, Profile, Documents, Applications, and About

### Recommendations and planning

- Configurable deterministic scoring for academic fit, programme relevance, eligibility, budget fit, profile strength, and application risk
- Eligibility states: `ELIGIBLE`, `MISSING_REQUIREMENTS`, `NOT_ELIGIBLE`, and `UNKNOWN`
- Profile Match percentages—explicitly **not** admission chances
- Estimated cost and budget compatibility
- What-if simulator API for changing CGPA, IELTS, budget, or countries without changing the stored profile
- Personalised action list from the advisor endpoint

### Documents and applications

- Resume upload for PDF, DOCX, and TXT files
- Draft resume extraction marked `AI_EXTRACTED_REVIEW_REQUIRED`
- Document vault API
- Add programmes to an application list and track initial `SHORTLISTED` status

## Data integrity promise

Abroadly deliberately separates authoritative programme facts from AI-generated guidance.

| Structured, source-backed data | AI-assisted or derived guidance |
| --- | --- |
| Programme name, university, country, tuition, deadlines, language requirements, source URL | Profile interpretation, explanation, roadmap guidance, resume extraction |
| Never invented by an LLM | Always presented as guidance and subject to review |

### Important MVP notice

The current catalogue is clearly labelled **SEED / DEMO DATA**. It exists to demonstrate the full product flow and must not be treated as production-verified admissions information. Students must confirm all requirements, costs, deadlines, and routes on the linked official university pages before applying.

## Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | React, TypeScript, Vite, Material UI |
| Backend | Python 3.12, FastAPI, Pydantic v2 |
| Data layer | SQLAlchemy 2.0, PostgreSQL, Alembic |
| Infrastructure | Docker Compose, Redis |
| Security | PBKDF2 password hashing, signed expiring bearer tokens |

## Architecture

```text
abroadly/
├── frontend/                  # React + Material UI web application
│   └── src/App.tsx            # Navigation, auth UI, dashboard, pages
├── backend/
│   ├── app/api/v1/            # FastAPI versioned endpoints
│   ├── app/core/              # Configuration, logging, token security
│   ├── app/dependencies/      # Authentication dependencies
│   ├── app/schemas/           # Pydantic request/response models
│   ├── app/services/          # Deterministic recommendation engine
│   └── alembic/               # Database migration setup
├── docker-compose.yml
└── .env.example
```

## Quick start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with the engine running
- Git (optional, for contributing)

### Run with Docker

```powershell
git clone https://github.com/AmoghShukla/Abroadly.git
cd Abroadly
Copy-Item .env.example .env
docker compose up --build
```

Open these URLs once the services are running:

| Service | URL |
| --- | --- |
| Web application | http://localhost:5173 |
| Interactive API documentation | http://localhost:8000/docs |
| API health check | http://localhost:8000/api/v1/health |

To stop the stack, press `Ctrl + C`, then run:

```powershell
docker compose down
```

## Environment variables

Copy `.env.example` to `.env` and set secure values before deployment.

```env
DATABASE_URL=postgresql+psycopg://abroadly:abroadly@postgres:5432/abroadly
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=
LOG_LEVEL=INFO
```

Never commit `.env` or production credentials.

## API overview

All API endpoints use the `/api/v1` prefix. Protected routes require:

```http
Authorization: Bearer <access_token>
```

| Area | Endpoint | Purpose |
| --- | --- | --- |
| System | `GET /health` | Check API availability |
| Auth | `POST /auth/register` | Create an account |
| Auth | `POST /auth/login` | Receive an access token |
| Profile | `GET /profile` / `PUT /profile` | Retrieve or save the student profile |
| Catalogue | `GET /programs` | Browse programmes; supports `country` and `field` query filters |
| Catalogue | `GET /programs/{program_id}` | View programme details |
| Matching | `POST /recommendations` | Generate profile-specific programme matches |
| Matching | `GET /recommendations/top10` | Retrieve saved-profile Top 10 results |
| Simulation | `POST /simulation` | Test alternate CGPA, IELTS, budget, or countries |
| Documents | `POST /documents/resume` | Upload and extract a resume draft |
| Documents | `GET /documents` | List uploaded documents |
| Applications | `POST /applications/{program_id}` | Add a programme to applications |
| Applications | `GET /applications` | List tracked applications |
| Advisor | `POST /ai/advisor` | Get prioritised next actions |

Full request and response schemas are available at `http://localhost:8000/docs` while the API is running.

## Recommendation philosophy

Abroadly does **not** say “you have an 85% chance of admission.”

Instead, it combines deterministic signals into a transparent **Profile Match**:

```text
Profile Match
├── Academic Fit
├── Programme Relevance
├── Eligibility Compatibility
├── Budget Fit
├── Profile Strength
└── Application Risk
```

This score helps students prioritise research and applications; the final admissions decision always belongs to the university.

## Development notes

The application is intentionally built in phases. The current MVP focuses on a complete profile → recommendations → documents/applications flow, rather than pretending its demo catalogue is a live admissions database.

Before production use, the following work is required:

- Replace in-memory MVP stores with normalised SQLAlchemy repositories and migrations
- Implement persistent refresh tokens, role-based access control, and secure document object storage
- Create verified ingestion adapters for DAAD, Study Australia, and official university sources
- Add source change history, data-review workflows, rate limiting, observability, and production tests
- Add transcript parsing, prerequisite mapping, and validated structured LLM providers
- Expand the country-adapter architecture to Canada, the UK, USA, Netherlands, Ireland, and beyond

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make focused changes and test them locally.
4. Commit using a clear message.
5. Open a pull request describing the problem, approach, and verification steps.

## Author

Built by **Amogh Shukla**.

---

If Abroadly helps you take the next step toward your Master's journey, consider starring the repository.
