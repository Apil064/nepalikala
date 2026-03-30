"""
Blog schemas.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
import uuid

from app.schemas.base import BaseResponseSchema


class PostStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class BlogCategoryBase(BaseModel):
    """Base blog category schema."""
    name: str
    slug: str
    description: Optional[str] = None


class BlogCategoryResponse(BlogCategoryBase, BaseResponseSchema):
    """Blog category response."""
    pass


class BlogPostBase(BaseModel):
    """Base blog post schema."""
    title: str
    subtitle: Optional[str] = None
    excerpt: Optional[str] = None
    content: str


class BlogPostCreate(BlogPostBase):
    """Blog post creation."""
    category_ids: List[uuid.UUID] = []
    tags: str = ""
    featured_artist_id: Optional[uuid.UUID] = None
    featured_artwork_id: Optional[uuid.UUID] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    is_premium: bool = False


class BlogPostUpdate(BaseModel):
    """Blog post update."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PostStatus] = None
    category_ids: Optional[List[uuid.UUID]] = None
    tags: Optional[str] = None
    is_featured: Optional[bool] = None


class AuthorSummary(BaseModel):
    """Author summary."""
    id: uuid.UUID
    name: str
    avatar_url: Optional[str] = None


class BlogPostResponse(BlogPostBase, BaseResponseSchema):
    """Blog post response."""
    slug: str
    author: Optional[AuthorSummary] = None
    author_name_override: Optional[str] = None
    categories: List[BlogCategoryResponse] = []
    featured_artist_id: Optional[uuid.UUID] = None
    featured_artwork_id: Optional[uuid.UUID] = None
    status: PostStatus
    published_at: Optional[datetime] = None
    featured_image_url: Optional[str] = None
    view_count: int
    like_count: int
    share_count: int
    is_featured: bool
    is_premium: bool
    reading_time_minutes: Optional[int] = None

    class Config:
        from_attributes = True


class BlogPostListResponse(BaseModel):
    """Paginated blog post list."""
    total: int
    page: int
    per_page: int
    total_pages: int
    items: List[BlogPostResponse]


class BlogPostFilterParams(BaseModel):
    """Blog post filter parameters."""
    category: Optional[str] = None
    status: Optional[PostStatus] = PostStatus.PUBLISHED
    is_featured: Optional[bool] = None
    author_id: Optional[uuid.UUID] = None
    search: Optional[str] = None
    sort_by: str = "-published_at"
    page: int = 1
    per_page: int = 20


class CommentCreate(BaseModel):
    """Comment creation."""
    content: str
    parent_id: Optional[uuid.UUID] = None


class CommentResponse(CommentCreate, BaseResponseSchema):
    """Comment response."""
    post_id: uuid.UUID
    author_id: Optional[uuid.UUID] = None
    author_name: str
    is_approved: bool
    is_featured: bool

    class Config:
        from_attributes = True
