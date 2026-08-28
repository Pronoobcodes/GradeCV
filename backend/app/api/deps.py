from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select 

from app.models.user import User
from app.core.security import decode_access_token
from app.db.db import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:

    credential_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    email = decode_access_token(token)
    if not email:
        raise credential_error
    
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active:
        raise credential_error
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user