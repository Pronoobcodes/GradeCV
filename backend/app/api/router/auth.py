from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.deps import get_session, get_current_active_user
from app.models import User
from app.core.security import create_access_token, create_verify_token
from app.schema.user import UserCreate, UserRead, PasswordResetRequest, PasswordResetConfirm
from app.services import (
    authenticate_user, 
    confirm_password_reset, 
    register_user, 
    request_password_reset
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session: Session = Depends(get_session)) -> User:
    try:
        user = register_user(session=session, user_create=user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login a user and return an access token"""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-verification", status_code=status.HTTP_200_OK)
def request_verification(
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_active_user)
):
    """Generates and triggers an email verification token for logged-in users."""
    try:
        token = create_verify_token(str(current_user.id))
        # TODO: Send email to user (e.g., send_verification_email(current_user.email, token))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Verification token sent to your email"}


@router.post("/password-reset/request", status_code=status.HTTP_200_OK)
def password_reset_request(payload: PasswordResetRequest, session: Session = Depends(get_session)):
    try:
        token = request_password_reset(session, payload.email)
    except ValueError:
        token = None
        
    response = {"message": "If that email is registered, a reset link has been sent."}
    if token:
        response["dev_token"] = token
    return response


@router.post("/password-reset/confirm", status_code=status.HTTP_200_OK)
def password_reset_confirm(payload: PasswordResetConfirm, session: Session = Depends(get_session)):
    if not confirm_password_reset(session, payload.token, payload.new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
    return {"message": "Password has been reset successfully"}
