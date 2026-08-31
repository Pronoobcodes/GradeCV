from fastapi import FastAPI

from app.api.router import auth, cvs, grading, job_descriptions, users
from app.core.middleware import setup_middleware

app = FastAPI(title="CV Grader", redirect_slashes=False)

setup_middleware(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cvs.router)
app.include_router(job_descriptions.router)
app.include_router(grading.router)