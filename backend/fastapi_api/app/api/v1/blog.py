"""
Blog endpoints.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.schemas.blog import (
    BlogPostResponse,
    BlogPostListResponse,
    BlogCategoryResponse,
    BlogPostFilterParams,
    PostStatus,
    CommentCreate,
    CommentResponse
)

router = APIRouter()


@router.get("/posts", response_model=BlogPostListResponse)
async def list_posts(
    category: str = None,
    status: PostStatus = PostStatus.PUBLISHED,
    is_featured: bool = None,
    author_id: UUID = None,
    search: str = None,
    sort_by: str = "-published_at",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List blog posts with filters.

    Query parameters:
    - category: Filter by category slug
    - status: Post status (default: published)
    - is_featured: Show only featured posts
    - author_id: Filter by author
    - search: Search in title and content
    - sort_by: Sort field
    - page: Page number
    - per_page: Items per page
    """
    return {
        "total": 24,
        "page": page,
        "per_page": per_page,
        "total_pages": 2,
        "items": [
            {
                "id": "post-1",
                "title": "The Secrets of Thangka Pigments",
                "slug": "secrets-thangka-pigments",
                "subtitle": "Discovering ancient techniques",
                "excerpt": "Exploring the natural pigments used in traditional Thangka painting...",
                "content": "Full article content here...",
                "author": {
                    "id": "user-1",
                    "name": "Editorial Team",
                    "avatar_url": None
                },
                "categories": [
                    {"id": "bcat-1", "name": "Tradition", "slug": "tradition"}
                ],
                "status": "published",
                "published_at": "2024-03-15T10:00:00",
                "featured_image_url": None,
                "view_count": 1842,
                "like_count": 45,
                "share_count": 12,
                "is_featured": True,
                "is_premium": False,
                "created_at": "2024-03-10T10:00:00",
                "updated_at": "2024-03-15T10:00:00",
                "is_active": True
            }
        ]
    }


@router.get("/posts/featured")
async def get_featured_posts(
    limit: int = Query(3, ge=1, le=10),
    db: AsyncSession = Depends(get_db)
):
    """Get featured posts for homepage."""
    return [
        {
            "id": "post-1",
            "title": "The Secrets of Thangka Pigments",
            "slug": "secrets-thangka-pigments",
            "excerpt": "Exploring the natural pigments used in traditional Thangka painting...",
            "author": "Editorial Team",
            "published_at": "2024-03-15",
            "featured_image_url": None,
            "view_count": 1842
        }
    ]


@router.get("/posts/{slug}", response_model=BlogPostResponse)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get single blog post by slug."""
    return {
        "id": "post-1",
        "title": "The Secrets of Thangka Pigments",
        "slug": slug,
        "subtitle": "Discovering ancient techniques",
        "excerpt": "Exploring the natural pigments used in traditional Thangka painting...",
        "content": "Full article content here with rich formatting...",
        "author": {
            "id": "user-1",
            "name": "Editorial Team",
            "avatar_url": None
        },
        "categories": [
            {"id": "bcat-1", "name": "Tradition", "slug": "tradition"}
        ],
        "status": "published",
        "published_at": "2024-03-15T10:00:00",
        "featured_image_url": None,
        "view_count": 1842,
        "like_count": 45,
        "share_count": 12,
        "is_featured": True,
        "is_premium": False,
        "reading_time_minutes": 8,
        "created_at": "2024-03-10T10:00:00",
        "updated_at": "2024-03-15T10:00:00",
        "is_active": True
    }


@router.post("/posts/{post_id}/view")
async def record_post_view(
    post_id: UUID,
    current_user: dict = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """Record post view."""
    return {"message": "View recorded"}


@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Like a blog post."""
    return {"message": "Post liked"}


# Categories
@router.get("/categories", response_model=List[BlogCategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    """List all blog categories."""
    return [
        {"id": "bcat-1", "name": "Tradition", "slug": "tradition"},
        {"id": "bcat-2", "name": "Folk Art", "slug": "folk-art"},
        {"id": "bcat-3", "name": "Contemporary", "slug": "contemporary"},
        {"id": "bcat-4", "name": "Craft", "slug": "craft"}
    ]


# Comments
@router.get("/posts/{post_id}/comments")
async def list_comments(
    post_id: UUID,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List comments for a post."""
    return {
        "total": 0,
        "page": page,
        "per_page": per_page,
        "items": []
    }


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: UUID,
    comment: CommentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create comment on a post."""
    return {
        "id": "comment-1",
        "post_id": str(post_id),
        "content": comment.content,
        "author_id": current_user.get("id"),
        "author_name": current_user.get("username"),
        "is_approved": False,
        "is_featured": False,
        "created_at": "2024-03-20T10:00:00"
    }
