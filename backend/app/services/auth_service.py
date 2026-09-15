from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password_hash,
)
from app.repositories.user_repository import(
    create_user,
    get_user_by_email
)


async def register_user(db: AsyncSession, user_data: UserRegister,) ->User:

    existing_user = await get_user_by_email(
        db=db, 
        email=user_data.email,
        )

    if existing_user is not None:
        raise ValueError("Email is already taken.")

    return await create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password)
    )

async def authenticate_user(db: AsyncSession, email: str, password: str)->User:
    user = await get_user_by_email(
        db=db,
        email=email,
    )
    if user is None:
        return None

    if not verify_password_hash(
        password,
        user.password_hash
    ):
        return None

    if not user .is_active:
        return None

    return user

def create_user_tokens(user: User)-> dict[str, str]:
    """
    Create access and refresh tokens for a user.
    """
    subject = str(user.id)

    return{
        "access_token": create_access_token(subject),
        "refresh_token": create_refresh_token(subject),
        "token_type": "bearer",
    }