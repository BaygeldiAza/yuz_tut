from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import (
    TokenResponse,
    UserRegister,
    UserLogin,
    UserResponse
)
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_user_tokens,
)

router = APIRouter (
    prefix="/auth",
    tags=["Authenticaton"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession=Depends(get_db)):
    try:
        user = await register_user(
            db=db,
            user_data=user_data,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    return user

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_202_ACCEPTED)
async def login(user_data: UserLogin, db:AsyncSession=Depends(get_db)):
    user = await authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_user_tokens(user)