"""
User schemas for authentication and user management.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
import uuid

from app.schemas.base import BaseResponseSchema


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    EDITOR = "editor"
    SUPPORT = "support"
    ARTIST = "artist"
    CUSTOMER = "customer"


class UserApplicationStatus(str, Enum):
    NOT_APPLIED = "not_applied"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    first_name: str = ""
    last_name: str = ""
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    """User registration schema."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CUSTOMER


class UserUpdate(BaseModel):
    """User update schema."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase, BaseResponseSchema):
    """User response schema."""
    role: UserRole
    is_verified: bool
    application_status: UserApplicationStatus
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class ArtistProfileBase(BaseModel):
    """Base artist profile schema."""
    bio: Optional[str] = None
    location: Optional[str] = None
    style: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[str] = None
    awards: Optional[str] = None
    exhibitions: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None


class ArtistProfileCreate(ArtistProfileBase):
    pass


class ArtistProfileResponse(ArtistProfileBase, BaseResponseSchema):
    """Artist profile response."""
    user_id: uuid.UUID
    display_name: str
    total_works: int
    total_sales: int
    revenue_npr: float
    portrait_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_verified: bool
    is_featured: bool


class ArtistApplicationCreate(BaseModel):
    """Artist application creation."""
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    location: str
    art_style: str
    years_experience: int
    portfolio_url: Optional[str] = None
    portfolio_description: str
    website: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordChangeRequest(BaseModel):
    """Password change request."""
    current_password: str
    new_password: str = Field(..., min_length=8)


class PasswordResetRequest(BaseModel):
    """Password reset request."""
    email: EmailStr


class UserListResponse(BaseModel):
    """Paginated user list."""
    total: int
    page: int
    per_page: int
    items: List[UserResponse]
