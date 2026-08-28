from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from app.core.settings import get_settings

settings = get_settings()

# ---- Password Hashing ----

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


# ---- JWT Access Tokens (Login Sessions) ----

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": str(subject), "exp": expire, "type": "access"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload.get("sub")
    except JWTError:
        return None


# ---- Password Reset Tokens ----

def create_password_reset_token(email: str) -> str:
    expiry_minutes = getattr(settings, "RESET_TOKEN_EXPIRY_MINUTES", 30)
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    to_encode = {"sub": str(email), "exp": expire, "type": "password_reset"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except JWTError:
        return None


# ---- Account Verification Tokens ----

def create_verify_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.VERIFY_TOKEN_EXPIRY_MINUTES)
    to_encode = {"sub": str(subject), "exp": expire, "type": "verify"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "verify":
            return None
        return payload.get("sub")
    except JWTError:
        return None
