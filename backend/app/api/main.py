from fastapi import FastAPI
from .router import auth, cvs, grading, job_descriptions, users

app = FastAPI(title="CV Grader")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cvs.router)
app.include_router(job_descriptions.router)
app.include_router(grading.router)
