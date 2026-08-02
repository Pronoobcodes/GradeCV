import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.grading import GradingResponse
from app.repositories.grading_repository import GradingRepository
from app.repositories.cv_repository import CVRepository
from app.services.grading_service import GradingService

router = APIRouter()

@router.post("/{cv_id}", response_model=GradingResponse)
async def evaluate_cv(
    cv_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv_repo = CVRepository(db)
    cv = await cv_repo.get_by_id(cv_id)
    
    if not cv or cv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="CV not found")
        
    grading_repo = GradingRepository(db)
    grading_service = GradingService(grading_repo)
    
    grading_record = await grading_service.grade_cv(cv, current_user.id)
    return grading_record

@router.get("/history", response_model=List[GradingResponse])
async def get_grading_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    grading_repo = GradingRepository(db)
    return await grading_repo.get_user_gradings(current_user.id)

@router.get("/{id}", response_model=GradingResponse)
async def get_grading(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    grading_repo = GradingRepository(db)
    grading = await grading_repo.get_by_id(id)
    
    if not grading or grading.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Grading record not found")
        
    return grading
