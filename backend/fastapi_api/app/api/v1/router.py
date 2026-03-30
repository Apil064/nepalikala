"""
Main API router aggregating all v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import auth, users, artworks, artists, orders, blog, admin

api_router = APIRouter()

# Public routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(artworks.router, prefix="/artworks", tags=["Artworks"])
api_router.include_router(artists.router, prefix="/artists", tags=["Artists"])
api_router.include_router(blog.router, prefix="/blog", tags=["Blog"])

# Protected routes
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])

# Admin routes
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])


@api_router.get("/")
async def api_root():
    """API root endpoint."""
    return {
        "name": "Nepaliकला API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/auth",
            "/api/v1/users",
            "/api/v1/artworks",
            "/api/v1/artists",
            "/api/v1/orders",
            "/api/v1/blog",
            "/api/v1/admin",
        ]
    }
