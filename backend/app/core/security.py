import jwt 
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from app.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hash plain password with Aaron2
    """

    return password_hash.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against its hashed
    """

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(subject: str, expires_minutes: int = settings.access_token_expire_minutes) ->str:
    """
    Create a JWT access token.
    Subject normally contains user_id UUID converted to string
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = {
        "sub": subject,
        "exp": expire,
        }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str)-> dict:
    """
    Decode and validate a JWT access token.
    """

    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )