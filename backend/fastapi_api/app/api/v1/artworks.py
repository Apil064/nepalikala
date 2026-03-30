"""
Artwork endpoints.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.schemas.artwork import (
    ArtworkResponse,
    ArtworkListResponse,
    ArtworkFilterParams,
    CategoryResponse,
    ArtworkType,
    ArtworkStatus
)

router = APIRouter()


@router.get("/", response_model=ArtworkListResponse)
async def list_artworks(
    category: str = None,
    artwork_type: ArtworkType = None,
    artist_id: UUID = None,
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    status: ArtworkStatus = ArtworkStatus.AVAILABLE,
    is_featured: bool = None,
    is_new_arrival: bool = None,
    search: str = None,
    sort_by: str = "-created_at",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List artworks with filters.

    Query parameters:
    - category: Filter by category slug
    - artwork_type: Filter by 'original' or 'print'
    - artist_id: Filter by artist ID
    - min_price/max_price: Price range filter
    - status: Artwork availability status
    - is_featured: Show only featured artworks
    - is_new_arrival: Show only new arrivals
    - search: Search in title and description
    - sort_by: Sort field (prefix with - for descending)
    - page: Page number
    - per_page: Items per page
    """
    # Mock response for demo
    return {
        "total": 401,
        "page": page,
        "per_page": per_page,
        "total_pages": 21,
        "items": [
            {
                "id": "p1",
                "title": "Himalayan Dawn Thangka",
                "slug": "himalayan-dawn-thangka",
                "description": "Natural pigments on cotton",
                "artwork_type": "original",
                "medium": "Natural pigments on cotton",
                "dimensions": "60×80 cm",
                "year_created": 2024,
                "price_npr": 85000,
                "price_usd": 650,
                "artist": {
                    "id": "artist-1",
                    "display_name": "Karma Lama",
                    "avatar_url": None,
                    "location": "Boudhanath, KTM",
                    "is_verified": True
                },
                "categories": [
                    {"id": "cat-1", "name": "Thangka", "slug": "thangka"}
                ],
                "status": "available",
                "edition_size": None,
                "edition_number": None,
                "prints_available": 0,
                "main_image_url": "/images/himalayan-dawn.jpg",
                "additional_images": [],
                "view_count": 245,
                "total_sales": 0,
                "is_featured": True,
                "is_new_arrival": False,
                "is_in_stock": True,
                "stock_display": "1",
                "created_at": "2024-03-01T10:00:00",
                "updated_at": "2024-03-01T10:00:00",
                "is_active": True
            }
        ]
    }


@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    """List all artwork categories."""
    return [
        {"id": "cat-1", "name": "Thangka", "slug": "thangka", "description": "Traditional Tibetan Buddhist paintings", "artwork_count": 48},
        {"id": "cat-2", "name": "Modern & Contemporary", "slug": "modern", "description": "Contemporary Nepali art", "artwork_count": 134},
        {"id": "cat-3", "name": "Madhubani", "slug": "madhubani", "description": "Traditional Mithila art", "artwork_count": 62},
        {"id": "cat-4", "name": "Sculpture & Craft", "slug": "sculpture", "description": "Sculptures and crafts", "artwork_count": 37},
        {"id": "cat-5", "name": "Digital Art", "slug": "digital", "description": "Digital artworks", "artwork_count": 29},
        {"id": "cat-6", "name": "Photography", "slug": "photography", "description": "Photography", "artwork_count": 91},
    ]


@router.get("/categories/{slug}", response_model=CategoryResponse)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get category by slug."""
    return {
        "id": "cat-1",
        "name": "Thangka",
        "slug": slug,
        "description": "Traditional Tibetan Buddhist paintings",
        "artwork_count": 48
    }


@router.get("/{artwork_id}", response_model=ArtworkResponse)
async def get_artwork(
    artwork_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get single artwork by ID."""
    return {
        "id": str(artwork_id),
        "title": "Himalayan Dawn Thangka",
        "slug": "himalayan-dawn-thangka",
        "description": "Natural pigments on cotton",
        "artwork_type": "original",
        "medium": "Natural pigments on cotton",
        "dimensions": "60×80 cm",
        "year_created": 2024,
        "price_npr": 85000,
        "price_usd": 650,
        "artist": {
            "id": "artist-1",
            "display_name": "Karma Lama",
            "avatar_url": None,
            "location": "Boudhanath, KTM",
            "is_verified": True
        },
        "categories": [
            {"id": "cat-1", "name": "Thangka", "slug": "thangka"}
        ],
        "status": "available",
        "edition_size": None,
        "edition_number": None,
        "prints_available": 0,
        "main_image_url": "/images/himalayan-dawn.jpg",
        "additional_images": [],
        "view_count": 245,
        "total_sales": 0,
        "is_featured": True,
        "is_new_arrival": False,
        "is_in_stock": True,
        "stock_display": "1",
        "created_at": "2024-03-01T10:00:00",
        "updated_at": "2024-03-01T10:00:00",
        "is_active": True
    }


@router.post("/{artwork_id}/view")
async def record_view(
    artwork_id: UUID,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """Record artwork view (for analytics)."""
    return {"message": "View recorded"}


@router.get("/{artwork_id}/related")
async def get_related_artworks(
    artwork_id: UUID,
    limit: int = 4,
    db: AsyncSession = Depends(get_db)
):
    """Get related artworks."""
    return {
        "items": []
    }
