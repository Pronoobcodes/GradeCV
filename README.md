# CV Grader

CV Grader is a full-stack app that scores how well a candidate's CV matches a job description and gives structured, actionable feedback — powered by an LLM.

- **Backend:** FastAPI + SQLModel + PostgreSQL, managed with `uv`
- **Frontend:** Next.js (App Router) + TypeScript + Tailwind CSS
- **Grading:** LLM-based scoring service, abstracted so the provider can be swapped

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Backend Structure & Rationale](#backend-structure--rationale)
- [Frontend Notes](#frontend-notes)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [1. Database Setup](#1-database-setup)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Running Everything Together](#4-running-everything-together)
- [Environment Variables](#environment-variables)
- [Grading / LLM Provider](#grading--llm-provider)
- [Deployment Notes](#deployment-notes)

---

## Architecture Overview

```
                         ┌────────────────────┐
                         │   PostgreSQL DB     │
                         │ (initialized via    │
                         │  TablePlus / psql)  │
                         └─────────▲──────────┘
                                   │
                         ┌─────────┴──────────┐
                         │   FastAPI Backend   │
                         │  (uv + SQLModel +   │
                         │   Alembic)          │
                         └─────────▲──────────┘
                                   │  REST API (JWT auth)
                         ┌─────────┴──────────┐
                         │  Next.js Frontend   │
                         │ (App Router + TS +  │
                         │  Tailwind)          │
                         └────────────────────┘
```

The frontend never talks to Postgres directly — it only talks to the FastAPI backend over HTTP, and the backend is the only thing with database credentials and the LLM API key.

---

## Backend Structure & Rationale

The backend lives in `backend/` and is organized by **responsibility**, not by feature, so that each layer only knows about the layer directly below it:

```
backend/
├── alembic/              # DB migrations (generated + versioned)
├── app/
│   ├── api/
│   │   ├── router/       # Route definitions, grouped by resource (auth, users, cvs, grading)
│   │   ├── deps.py        # Shared FastAPI dependencies (current_user, db session, etc.)
│   │   └── main.py        # Wires all routers into the FastAPI app
│   ├── core/
│   │   ├── middleware.py  # CORS + error/logging middleware
│   │   ├── security.py    # Password hashing, JWT create/verify
│   │   └── settings.py    # Pydantic-settings config, reads from .env
│   ├── db/
│   │   ├── database.py    # SQLModel engine creation
│   │   └── db.py           # Session factory / get_session dependency
│   ├── models/            # SQLModel table models (the actual DB schema)
│   ├── schema/             # Pydantic request/response schemas (NOT the same as models)
│   ├── services/           # Business logic (auth, CV parsing, grading) — framework-agnostic
│   └── utils/               # Small stateless helpers (e.g. PDF text extraction)
├── .env
├── alembic.ini
├── pyproject.toml          # uv-managed dependencies
└── uv.lock
```

**Why it's structured this way:**

- **`models/` vs `schema/` are kept separate on purpose.** `models/` defines what's actually stored in Postgres (SQLModel table classes, with relationships and constraints). `schema/` defines what the API accepts and returns (Pydantic classes for `Create`, `Read`, `Update` variants). Merging these two would leak internal DB fields (like password hashes or internal foreign keys) straight into API responses, and would make it impossible to have a request shape that differs from the stored shape (e.g. accepting a plaintext password on register but never returning it).
- **`services/` exists so routes stay thin.** Route handlers in `api/router/` only parse the request, call a service function, and return the response. All the actual logic — hashing a password, extracting text from a PDF, calling the LLM and parsing its JSON — lives in `services/`. This makes the logic independently testable without spinning up FastAPI, and means the grading logic isn't tied to any one route.
- **`core/security.py` is isolated from `core/settings.py`** so that secrets/config loading and actual crypto logic aren't mixed in the same file — makes it easier to audit the security-sensitive code on its own.
- **`db/database.py` and `db/db.py` are split** so the engine (a single, expensive-to-create object) is created once, while the session dependency (`get_session`) is what's actually injected per-request into routes — this avoids leaking connections and matches how SQLModel/SQLAlchemy expects sessions to be scoped.
- **Alembic is used instead of `SQLModel.metadata.create_all()`** so schema changes are versioned and reversible — important once there's real user data in Postgres, since `create_all` can't handle altering or dropping columns safely.
- **`uv` instead of `pip`/`poetry`** for faster, reproducible installs — `pyproject.toml` + `uv.lock` pin exact versions so the environment is identical between machines.

---

## Frontend Notes

**The frontend was built almost entirely by AI (Claude), driven by prompts rather than hand-written code.** Concretely, that means:

- The visual design (colors, fonts, spacing, component shapes) wasn't hand-picked — it was **derived from a folder of reference images** provided to the AI, which extracted a palette and typography (Playfair Display for headings, Plus Jakarta Sans for UI text) and turned it into a `DESIGN.md` + Tailwind theme before any component was built.
- Every page (landing, auth, grading form, history) and every reusable component (`Button`, `Card`, `FileUpload`, `ScoreGauge`, `Badge`, etc.) was generated step-by-step from a structured prompt, reviewed stage by stage rather than all at once.
- Because of this, if you're extending the frontend, it's worth **re-using the same prompt-driven approach** (see `/prompts` if included, or the project notes) rather than hand-rolling new styles that might drift from the existing design system in `DESIGN.md`.
- A few issues that came up during AI-driven generation and had to be explicitly fixed afterward: layout/alignment bugs in generated sections, a hydration warning caused by a browser extension injecting attributes into `<body>` (fixed with `suppressHydrationWarning`), and a file-upload bug in the Next.js API proxy route that silently broke CV submissions. These are the kinds of issues to watch for if you regenerate or extend sections with AI — always test the actual network request, not just the UI rendering.

---

## Setup

### Prerequisites

- Python 3.11+ and [`uv`](https://docs.astral.sh/uv/) installed
- Node.js 18+ and npm
- PostgreSQL running locally (via [TablePlus](https://tableplus.com/), `psql`, Postgres.app, or Docker)
- An API key for whichever LLM provider you're using for grading (see [Grading / LLM Provider](#grading--llm-provider))

### 1. Database Setup

Using TablePlus (or any Postgres GUI):

1. Connect to your local Postgres server.
2. Create a new database, e.g. `cv_grader`.
3. Note the connection details (host, port, username, password, database name) — you'll put these into the backend `.env` as `DATABASE_URL`.

Example connection string format:
```
DATABASE_URL=postgresql://username:password@localhost:5432/cv_grader
```

### 2. Backend Setup

```bash
cd backend
uv sync                     # installs dependencies from pyproject.toml / uv.lock
cp .env.example .env        # then fill in DATABASE_URL, JWT secret, LLM API key, etc.
uv run alembic upgrade head # applies all migrations to your Postgres DB
uv run uvicorn app.api.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

The app will be available at `http://localhost:3000`.

### 4. Running Everything Together

Run the backend and frontend in two separate terminals (both commands above use `--reload`/`dev` so changes hot-reload). Make sure Postgres is running before starting the backend, and that the backend is running before using the frontend's grading/auth features.

---

## Environment Variables

**Backend (`backend/.env`):**

| Variable | Description |
|---|---|
| `DATABASE_URL` | Postgres connection string |
| `JWT_SECRET_KEY` | Secret used to sign JWTs |
| `JWT_ALGORITHM` | e.g. `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime |
| `LLM_PROVIDER` | Which grading provider to use (e.g. `groq`, `gemini`, `openrouter`) |
| `LLM_API_KEY` | API key for the chosen provider |

**Frontend (`frontend/.env.local`):**

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Base URL of the FastAPI backend |

---

## Grading / LLM Provider

The grading logic lives entirely in `backend/app/services/`, behind a single function so the provider can be swapped without touching routes or schemas. During development, a **free-tier LLM** (e.g. Groq, Google Gemini free tier, or an OpenRouter free model) is used to avoid cost while iterating. See the grading service for the exact prompt used and the JSON contract it expects back (`score`, `matched_skills`, `missing_skills`, `feedback`).

## Deployment Notes

Before deploying:
- Swap the local Postgres connection for a hosted instance (e.g. Supabase, Neon, Railway).
- Re-evaluate the LLM provider for production rate limits/cost — a free tier suitable for development may not hold up under real traffic.
- Update CORS origins in `core/middleware.py` to the deployed frontend domain.
- Set all secrets (JWT secret, LLM API key, DB credentials) as environment variables on the hosting platform rather than committing `.env`.