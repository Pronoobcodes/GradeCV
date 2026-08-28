from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_active_user, get_session
from app.models import User
from app.schema.user import PasswordChange, UserProfileUpdate, UserRead
from app.services import change_password
from app.services.auth_service import get_user_by_email

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):

    if hasattr(payload, 'email') and payload.email and payload.email != current_user.email:
        if get_user_by_email(session, payload.email):
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = payload.email
        
    if payload.full_name is not None:
        current_user.full_name = payload.full_name

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.post("/me/change-password")
def change_my_password(
    payload: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    try:
        change_password(session, current_user, payload.current_password, payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed successfully"}
