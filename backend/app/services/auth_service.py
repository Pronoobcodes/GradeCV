from sqlmodel import Session, select

from app.core.security import create_password_reset_token, hash_password, verify_password, verify_password_reset_token
from app.models import User
from app.schema.user import UserCreate


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def register_user(session: Session, user_create: UserCreate) -> User:
    if get_user_by_email(session, user_create.email):
        raise ValueError("User with this email already exists")
    hashed_password = hash_password(user_create.password)
    user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def change_password(session: Session, user: User, new_password: str, current_password: str) -> User:
    if not verify_password(current_password, user.hashed_password):
        raise ValueError("Incorrect current password")
    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()
    

def request_password_reset(session: Session, email: str) -> str:
    user = get_user_by_email(session, email)
    if not user:
        raise ValueError("User not found")
    token = create_password_reset_token(email)
    # TODO: Send email to user
    return token
    

def confirm_password_reset(session: Session, token: str, new_password: str) -> bool:
    email = verify_password_reset_token(token)
    if not email:
        return False
    user = get_user_by_email(session, email)
    if not user:
        return False
    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()
    return True