# GradeCV Backend

GradeCV is a production-ready, AI-powered CV/Resume grading platform backend built with FastAPI, SQLModel, PostgreSQL, and OpenAI.

## Overview
Users upload their CVs (PDF or DOCX), and the system extracts the text, stores the CV, evaluates the content via an AI model (and heuristic ATS scoring), and stores a detailed grading history.

## Architecture
The project strictly follows Clean Architecture principles:
- **Routes**: No business logic, handle HTTP requests/responses.
- **Services**: Contain all business logic (auth, AI grading, parsing, ATS scoring).
- **Repositories**: Handle database interactions via SQLModel.
- **Database**: PostgreSQL accessed asynchronously.

## Folder Structure
```
app/
├── api/             # FastAPI routers and dependencies
├── core/            # Config, security, logging
├── db/              # Session, base models, init script
├── models/          # SQLModel database models
├── repositories/    # Database CRUD operations
├── schemas/         # Pydantic validation schemas
├── services/        # Business logic (AI, parsing, auth)
├── utils/           # Helper functions
└── main.py          # FastAPI application entrypoint
```

## Technology Stack
- **Framework**: FastAPI
- **ORM**: SQLModel / SQLAlchemy
- **Database**: PostgreSQL with AsyncPG
- **Migrations**: Alembic
- **Parsers**: PyMuPDF (PDF), python-docx (DOCX)
- **Security**: Passlib (bcrypt), python-jose (JWT)
- **AI**: OpenAI Python SDK
- **Package Manager**: uv

## Installation & Setup

1. **Install Dependencies (using uv)**
   ```bash
   uv sync
   ```

2. **Database Setup**
   - Install PostgreSQL locally.
   - Create a database: `CREATE DATABASE gradecv;`
   - Create an `.env` file from `.env.example` and fill in the database credentials (e.g., username `postgres` and your password).

3. **Running Migrations (Alembic)**
   Ensure the database is running and credentials are in your `.env`, then run:
   ```bash
   uv run alembic revision --autogenerate -m "init"
   uv run alembic upgrade head
   ```

4. **Running the Server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

5. **Running Tests**
   ```bash
   uv run pytest
   ```

## API Documentation
Once the server is running, visit `http://127.0.0.1:8000/docs` to view the interactive Swagger API documentation.

### Authentication Flow
1. `POST /api/v1/auth/register` - Create an account.
2. `POST /api/v1/auth/login` - Obtain a JWT access token.
3. Use the token in the `Authorization: Bearer <token>` header for protected routes.

## Limitations
- AI grading depends on the quality and consistency of the language model's responses.
- ATS scoring is heuristic-based and does not guarantee compatibility with every commercial ATS.
- Only PDF and DOCX uploads are supported.
- Maximum upload size is 10 MB.
- Local PostgreSQL is required during development.
- AI analysis requires a valid API key.
- No frontend is included.
- No background task queue is implemented initially.
- No email verification or password reset in the first version.
- Rate limiting is not yet implemented.

## Future Improvements
- Implement Celery/Redis for background AI processing.
- Add robust rate limiting (e.g., slowapi).
- Implement email verification and password reset flows.
- Containerize the application with Docker and Docker Compose.
