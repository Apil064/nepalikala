"""
Authentication endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    PasswordChangeRequest,
    PasswordResetRequest,
    ArtistApplicationCreate
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user account."""
    # This would normally check if user exists, create user, etc.
    # For demo, return mock data
    user = {
        "id": "mock-uuid",
        "email": user_data.email,
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "role": user_data.role.value,
        "is_verified": False,
        "is_active": True,
    }

    access_token = create_access_token(
        data={"sub": user["id"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token."""
    # This would normally verify credentials against database
    # For demo, return mock data
    user = {
        "id": "mock-uuid",
        "email": credentials.email,
        "username": "demo_user",
        "first_name": "Demo",
        "last_name": "User",
        "role": "customer",
        "is_verified": True,
        "is_active": True,
    }

    access_token = create_access_token(
        data={"sub": user["id"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }


@router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user)
):
    """Logout current user."""
    # In a stateless JWT setup, logout is handled client-side
    # Server-side could add token to blacklist if needed
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user)
):
    """Get current authenticated user info."""
    return current_user


@router.post("/refresh")
async def refresh_token(
    current_user: dict = Depends(get_current_user)
):
    """Refresh access token."""
    new_token = create_access_token(
        data={"sub": current_user["id"], "role": current_user.get("role", "customer")},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/password/change")
async def change_password(
    data: PasswordChangeRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password."""
    return {"message": "Password changed successfully"}


@router.post("/password/reset-request")
async def request_password_reset(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset email."""
    return {"message": "Password reset instructions sent to email"}


@router.post("/apply-artist", status_code=status.HTTP_201_CREATED)
async def apply_artist(
    application: ArtistApplicationCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit artist application."""
    return {
        "message": "Artist application submitted successfully",
        "application_id": "mock-application-id",
        "status": "pending"
    }
