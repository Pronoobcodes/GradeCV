from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.deps import get_session
from app.core.security import create_access_token
from app.schema.user import UserCreate, UserRead, PasswordResetRequest, PasswordResetConfirm, PasswordChange
from app.services import authenticate_user, confirm_password_reset, register_user, get_user_by_email, request_password_reset, change_password

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    try:
        user = register_user(session=session, user_create=user_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 
        
        
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login a user and return an access token"""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-reset")
def request_password_reset_endpoint(password_reset_request: PasswordResetRequest, session: Session = Depends(get_session)):
    try:
        token = request_password_reset(session, password_reset_request.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password reset token sent to your email"}

@router.post("/confirm-password-reset")
def confirm_password_reset_endpoint(password_reset_confirm: PasswordResetConfirm, session: Session = Depends(get_session)):
    try:
        success = confirm_password_reset(session, password_reset_confirm.token, password_reset_confirm.new_password)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid or expired password reset token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password reset successful"}

@router.post("/change-password")
def change_password_endpoint(password_change: PasswordChange, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    try:
        change_password(session, current_user, password_change.new_password, password_change.current_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed successfully"}

@router.post("/request-verification")
def request_verification(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    try:
        token = create_verify_token(str(current_user.id))
        # TODO: Send email to user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Verification token sent to your email"}