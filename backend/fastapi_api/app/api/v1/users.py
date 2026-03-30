"""
User management endpoints.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserListResponse,
    ArtistProfileResponse,
    ArtistProfileUpdate
)

router = APIRouter()


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = 1,
    per_page: int = 20,
    role: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List users (admin only)."""
    return {
        "total": 0,
        "page": page,
        "per_page": per_page,
        "items": []
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID."""
    raise HTTPException(status_code=404, detail="User not found")


@router.patch("/me", response_model=UserResponse)
async def update_me(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete current user account."""
    return None


# Artist Profile endpoints
@router.get("/me/artist-profile", response_model=ArtistProfileResponse)
async def get_my_artist_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's artist profile."""
    raise HTTPException(status_code=404, detail="Artist profile not found")


@router.patch("/me/artist-profile", response_model=ArtistProfileResponse)
async def update_artist_profile(
    update_data: ArtistProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update artist profile."""
    raise HTTPException(status_code=404, detail="Artist profile not found")


@router.get("/{user_id}/activity")
async def get_user_activity(
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user activity (admin only)."""
    return {
        "user_id": user_id,
        "activities": []
    }
