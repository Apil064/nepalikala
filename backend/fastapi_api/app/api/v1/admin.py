"""
Admin endpoints for dashboard data.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import UserRole

router = APIRouter()


def require_admin(user: dict):
    """Check if user has admin privileges."""
    if user.get("role") not in [UserRole.SUPER_ADMIN.value, UserRole.ADMIN.value]:
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics."""
    require_admin(current_user)

    return {
        "revenue": {
            "this_month": 840000,
            "last_month": 730000,
            "trend": "+14%"
        },
        "orders": {
            "this_month": 186,
            "last_month": 152,
            "pending": 28,
            "trend": "+22%"
        },
        "artists": {
            "total": 120,
            "new_applications": 5,
            "trend": "+8%"
        },
        "countries": {
            "this_month": 42,
            "top": ["USA", "UK", "Germany", "India", "Japan"]
        },
        "recent_orders": [
            {
                "id": "ord-1042",
                "customer": "Anna M.",
                "country": "Germany",
                "artwork": "Himalayan Dawn Thangka",
                "artist": "Karma Lama",
                "amount": 85000,
                "status": "processing",
                "date": "2024-03-19"
            }
        ]
    }


@router.get("/analytics")
async def get_analytics(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics data."""
    require_admin(current_user)

    return {
        "page_views": {
            "total": 48200,
            "trend": "+31%"
        },
        "visitors": {
            "unique": 12450,
            "trend": "+18%"
        },
        "session_duration": "3m 42s",
        "bounce_rate": "42%",
        "top_pages": [
            {"page": "Home", "views": 18400, "time": "1m 12s", "conversion": "3.2%"},
            {"page": "Shop", "views": 9800, "time": "4m 22s", "conversion": "6.8%"},
            {"page": "Product Detail", "views": 7200, "time": "5m 10s", "conversion": "8.4%"}
        ],
        "top_countries": [
            {"country": "United States", "sessions": 3200, "revenue": 210000, "avg_order": 14200},
            {"country": "United Kingdom", "sessions": 1800, "revenue": 140000, "avg_order": 18500}
        ]
    }


@router.get("/revenue")
async def get_revenue_report(
    start_date: str = None,
    end_date: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get revenue report."""
    require_admin(current_user)

    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "summary": {
            "total_revenue": 840000,
            "total_orders": 186,
            "average_order_value": 4516,
            "platform_fees": 168000,
            "artist_payouts": 672000
        },
        "by_category": [
            {"category": "Thangka", "revenue": 294000, "percentage": 35},
            {"category": "Modern", "revenue": 176400, "percentage": 21},
            {"category": "Photography", "revenue": 134400, "percentage": 16}
        ],
        "daily_breakdown": []
    }


@router.get("/artists/top")
async def get_top_artists(
    limit: int = Query(10, ge=1, le=50),
    period: str = Query("month", regex="^(week|month|year|all)$"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get top performing artists."""
    require_admin(current_user)

    return [
        {"rank": 1, "artist": "Karma Lama", "sales": 8, "revenue": 240000},
        {"rank": 2, "artist": "Priya Gurung", "sales": 22, "revenue": 180000},
        {"rank": 3, "artist": "Geeta Devi", "sales": 11, "revenue": 120000}
    ]


@router.get("/inventory")
async def get_inventory_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get inventory status."""
    require_admin(current_user)

    return {
        "total_artworks": 401,
        "available": 342,
        "sold": 48,
        "reserved": 11,
        "low_stock_alerts": [
            {"artwork": "Everest Spirit Print", "remaining": 3}
        ],
        "out_of_stock": []
    }


@router.post("/orders/{order_id}/status")
async def update_order_status(
    order_id: UUID,
    status: str,
    notes: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update order status (admin)."""
    require_admin(current_user)

    return {
        "message": "Order status updated",
        "order_id": str(order_id),
        "new_status": status
    }


@router.get("/applications/artists")
async def list_artist_applications(
    status: str = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List artist applications."""
    require_admin(current_user)

    return {
        "total": 5,
        "page": page,
        "per_page": per_page,
        "items": [
            {
                "id": "app-1",
                "name": "Anita Shrestha",
                "location": "Pokhara",
                "style": "Watercolour",
                "years": 8,
                "status": "pending",
                "applied_at": "2024-03-19"
            }
        ]
    }


@router.post("/applications/artists/{app_id}/approve")
async def approve_artist_application(
    app_id: UUID,
    notes: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Approve artist application."""
    require_admin(current_user)

    return {"message": "Application approved", "application_id": str(app_id)}


@router.post("/applications/artists/{app_id}/reject")
async def reject_artist_application(
    app_id: UUID,
    reason: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Reject artist application."""
    require_admin(current_user)

    return {"message": "Application rejected", "application_id": str(app_id)}
