import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_current_active_user, get_session
from app.models import CV, GradingResult, JobDescription, User
from app.schema.grading_result import GradingResultCreate, GradingResultRead
from app.services import grade_cv_against_job

router = APIRouter(prefix="/grading", tags=["grading"])

@router.post("", response_model=GradingResultRead, status_code=201)
def create_grading(
    payload: GradingResultCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    cv = session.get(CV, payload.cv_id)
    if not cv or cv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="CV not found")

    jd = session.get(JobDescription, payload.job_description_id)
    if not jd or jd.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job description not found")

    try:
        result = grade_cv_against_job(cv.file_content, jd.content)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Grading service error: {e}")

    grading = GradingResult(
        user_id=current_user.id,
        cv_id=cv.id,
        job_description_id=jd.id,
        score=result["score"],
        feedback=result["feedback"],
        raw_llm_response=result["raw_llm_response"],
    )
    session.add(grading)
    session.commit()
    session.refresh(grading)
    return grading

@router.get("", response_model=list[GradingResultRead])
def list_gradings(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(GradingResult).where(GradingResult.user_id == current_user.id)).all()
