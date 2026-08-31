from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session, select

from app.api.deps import get_current_active_user, get_session
from app.models import CV, User
from app.schema.cv import CVRead, CVReadDetail
from app.services.cv_parsing_service import extract_text_from_pdf


router = APIRouter(prefix="/cvs", tags=["cvs"])


@router.post("", response_model=CVReadDetail, status_code=201)
async def create_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    extracted_text = extract_text_from_pdf(await file.read())
    if not extracted_text:
        raise HTTPException(status_code=422, detail="could not extract any text from this pdf")

    cv = CV(user_id=current_user.id, filename=file.filename, file_content=extracted_text)
    session.add(cv)
    session.commit()
    session.refresh(cv)
    return cv


@router.get("", response_model=list[CVRead])
def read_cvs(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    cvs = session.exec(select(CV).where(CV.user_id == current_user.id)).all()
    return cvs


@router.get("/{cv_id}", response_model=CVReadDetail)
def read_cv(
    cv_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    cv = session.get(CV, cv_id)
    if not cv or cv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv
    
    
    
