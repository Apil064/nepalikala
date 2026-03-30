"""
Artwork schemas for the art marketplace.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel, Field
import uuid

from app.schemas.base import BaseResponseSchema


class ArtworkType(str, Enum):
    ORIGINAL = "original"
    PRINT = "print"


class ArtworkStatus(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    RESERVED = "reserved"
    COMING_SOON = "coming_soon"


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    slug: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase, BaseResponseSchema):
    """Category response."""
    image_url: Optional[str] = None
    artwork_count: int = 0


class ArtworkBase(BaseModel):
    """Base artwork schema."""
    title: str
    description: str
    artwork_type: ArtworkType
    medium: Optional[str] = None
    dimensions: Optional[str] = None
    year_created: Optional[int] = None
    price_npr: Decimal = Field(..., ge=0)
    price_usd: Optional[Decimal] = Field(None, ge=0)


class ArtworkCreate(ArtworkBase):
    """Artwork creation schema."""
    artist_id: uuid.UUID
    category_ids: List[uuid.UUID] = []
    edition_size: Optional[int] = None
    edition_number: Optional[str] = None
    prints_available: int = 0


class ArtworkUpdate(BaseModel):
    """Artwork update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    artwork_type: Optional[ArtworkType] = None
    medium: Optional[str] = None
    dimensions: Optional[str] = None
    year_created: Optional[int] = None
    price_npr: Optional[Decimal] = Field(None, ge=0)
    price_usd: Optional[Decimal] = Field(None, ge=0)
    status: Optional[ArtworkStatus] = None
    category_ids: Optional[List[uuid.UUID]] = None
    prints_available: Optional[int] = None
    is_featured: Optional[bool] = None
    is_new_arrival: Optional[bool] = None


class ArtistSummary(BaseModel):
    """Artist summary for artwork responses."""
    id: uuid.UUID
    display_name: str
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool


class CategorySummary(BaseModel):
    """Category summary for artwork responses."""
    id: uuid.UUID
    name: str
    slug: str


class ArtworkResponse(ArtworkBase, BaseResponseSchema):
    """Artwork response schema."""
    slug: str
    artist: ArtistSummary
    categories: List[CategorySummary]
    status: ArtworkStatus
    edition_size: Optional[int] = None
    edition_number: Optional[str] = None
    prints_available: int
    main_image_url: Optional[str] = None
    additional_images: List[str] = []
    view_count: int
    total_sales: int
    is_featured: bool
    is_new_arrival: bool
    is_in_stock: bool
    stock_display: str

    class Config:
        from_attributes = True


class ArtworkListResponse(BaseModel):
    """Paginated artwork list."""
    total: int
    page: int
    per_page: int
    total_pages: int
    items: List[ArtworkResponse]


class ArtworkFilterParams(BaseModel):
    """Artwork filter parameters."""
    category: Optional[str] = None
    artwork_type: Optional[ArtworkType] = None
    artist_id: Optional[uuid.UUID] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    status: Optional[ArtworkStatus] = ArtworkStatus.AVAILABLE
    is_featured: Optional[bool] = None
    search: Optional[str] = None
    sort_by: str = "-created_at"
    page: int = 1
    per_page: int = 20


class ArtistCreate(BaseModel):
    """Artist creation schema."""
    user_id: uuid.UUID
    bio: str
    location: Optional[str] = None
    style: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[str] = None
    awards: Optional[str] = None
    exhibitions: Optional[str] = None


class ArtistUpdate(BaseModel):
    """Artist update schema."""
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
    twitter: Optional[str] = None
    is_verified: Optional[bool] = None
    is_featured: Optional[bool] = None


class ArtistResponse(ArtistCreate, BaseResponseSchema):
    """Artist response."""
    display_name: str
    total_works: int
    total_sales: int
    revenue_npr: Decimal
    portrait_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ArtistListResponse(BaseModel):
    """Paginated artist list."""
    total: int
    page: int
    per_page: int
    total_pages: int
    items: List[ArtistResponse]


class ArtistFilterParams(BaseModel):
    """Artist filter parameters."""
    style: Optional[str] = None
    location: Optional[str] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    search: Optional[str] = None
    sort_by: str = "-total_sales"
    page: int = 1
    per_page: int = 20
