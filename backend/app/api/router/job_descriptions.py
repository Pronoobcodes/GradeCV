from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.api.deps import get_current_active_user, get_session
from app.models import JobDescription, User
from app.schema.job_description import JobDescriptionCreate, JobDescriptionRead

router = APIRouter(prefix="/job-descriptions", tags=["job-descriptions"])

@router.post("/", response_model=JobDescriptionRead, status_code=201)
def create_job_description(
    payload: JobDescriptionCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    jd = JobDescription(user_id=current_user.id, title=payload.title, content=payload.content)
    session.add(jd)
    session.commit()
    session.refresh(jd)
    return jd

@router.get("/", response_model=list[JobDescriptionRead])
def list_job_descriptions(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(JobDescription).where(JobDescription.user_id == current_user.id)).all()
