import uuid
import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.cv import CVResponse, CVResponseWithText, CVCreate
from app.repositories.cv_repository import CVRepository
from app.utils.helpers import save_upload_file, generate_unique_filename
from app.utils.validators import validate_file_type, validate_file_size
from app.services.cv_parser import CVParserService

router = APIRouter()

@router.post("/upload", response_model=CVResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_file_type(file.filename)
    validate_file_size(file)
    
    unique_filename = generate_unique_filename(file.filename)
    file_path = await save_upload_file(file, unique_filename)
    
    # Extract text immediately or enqueue a background task
    # For now, we do it synchronously to store it
    file_type = unique_filename.split('.')[-1]
    
    try:
        extracted_text = CVParserService.extract_text(file_path, file_type)
    except Exception as e:
        # Cleanup if parsing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing file: {str(e)}"
        )
        
    cv_repo = CVRepository(db)
    
    cv_in = CVCreate(
        original_filename=file.filename,
        file_type=file_type,
        stored_filename=unique_filename,
        file_path=file_path,
        extracted_text=extracted_text,
        user_id=current_user.id
    )
    
    cv = await cv_repo.create(cv_in)
    return cv

@router.get("", response_model=List[CVResponse])
async def get_user_cvs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv_repo = CVRepository(db)
    return await cv_repo.get_user_cvs(current_user.id)

@router.get("/{id}", response_model=CVResponseWithText)
async def get_cv(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv_repo = CVRepository(db)
    cv = await cv_repo.get_by_id(id)
    if not cv or cv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv_repo = CVRepository(db)
    cv = await cv_repo.get_by_id(id)
    if not cv or cv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="CV not found")
        
    # delete file from disk
    if os.path.exists(cv.file_path):
        os.remove(cv.file_path)
        
    await cv_repo.delete(id)
    return None
