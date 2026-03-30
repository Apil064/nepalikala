"""
Artist endpoints.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.schemas.artwork import (
    ArtistResponse,
    ArtistListResponse,
    ArtistFilterParams
)
from app.schemas.artwork import ArtworkListResponse

router = APIRouter()


@router.get("/", response_model=ArtistListResponse)
async def list_artists(
    style: str = None,
    location: str = None,
    is_featured: bool = None,
    is_verified: bool = None,
    search: str = None,
    sort_by: str = "-total_sales",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List artists with filters.

    Query parameters:
    - style: Filter by art style (Thangka, Modern, Madhubani, etc.)
    - location: Filter by location
    - is_featured: Show only featured artists
    - is_verified: Show only verified artists
    - search: Search in name, bio, or style
    - sort_by: Sort field (total_sales, -created_at, etc.)
    - page: Page number
    - per_page: Items per page
    """
    # Mock response
    return {
        "total": 120,
        "page": page,
        "per_page": per_page,
        "total_pages": 6,
        "items": [
            {
                "id": "artist-1",
                "display_name": "Karma Lama",
                "bio": "Master Thangka painter with 20 years of experience",
                "location": "Boudhanath, KTM",
                "style": "Thangka",
                "years_experience": 20,
                "total_works": 24,
                "total_sales": 45,
                "revenue_npr": 820000,
                "portrait_url": None,
                "cover_image_url": None,
                "is_verified": True,
                "is_featured": True
            }
        ]
    }


@router.get("/featured")
async def get_featured_artists(
    limit: int = Query(4, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Get featured artists for homepage."""
    return [
        {
            "id": "artist-1",
            "display_name": "Karma Lama",
            "style": "Thangka",
            "location": "Boudhanath, KTM",
            "total_works": 24,
            "portrait_url": None,
            "is_verified": True
        },
        {
            "id": "artist-2",
            "display_name": "Sita Maharjan",
            "style": "Oil & Acrylic",
            "location": "Lalitpur, Patan",
            "total_works": 18,
            "portrait_url": None,
            "is_verified": True
        },
        {
            "id": "artist-3",
            "display_name": "Geeta Devi",
            "style": "Madhubani",
            "location": "Janakpur",
            "total_works": 31,
            "portrait_url": None,
            "is_verified": True
        },
        {
            "id": "artist-4",
            "display_name": "Anil Tamang",
            "style": "Digital",
            "location": "Thamel, KTM",
            "total_works": 40,
            "portrait_url": None,
            "is_verified": True
        }
    ]


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get single artist by ID."""
    return {
        "id": str(artist_id),
        "display_name": "Karma Lama",
        "bio": "Master Thangka painter with 20 years of experience",
        "location": "Boudhanath, KTM",
        "style": "Thangka",
        "years_experience": 20,
        "education": "Traditional apprenticeship",
        "awards": "National Art Award 2020",
        "exhibitions": "Solo exhibitions in Kathmandu, Delhi, New York",
        "total_works": 24,
        "total_sales": 45,
        "revenue_npr": 820000,
        "portrait_url": None,
        "cover_image_url": None,
        "is_verified": True,
        "is_featured": True,
        "user_id": "user-1",
        "created_at": "2022-01-01T10:00:00",
        "updated_at": "2024-03-01T10:00:00",
        "is_active": True
    }


@router.get("/{artist_id}/artworks", response_model=ArtworkListResponse)
async def get_artist_artworks(
    artist_id: UUID,
    status: str = "available",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get artworks by artist."""
    return {
        "total": 24,
        "page": page,
        "per_page": per_page,
        "total_pages": 2,
        "items": []
    }


@router.get("/{artist_id}/stats")
async def get_artist_stats(
    artist_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get artist statistics."""
    return {
        "total_works": 24,
        "total_sales": 45,
        "revenue_npr": 820000,
        "revenue_this_month": 125000,
        "views_this_month": 1200,
        "top_countries": ["USA", "UK", "Germany", "India"]
    }
