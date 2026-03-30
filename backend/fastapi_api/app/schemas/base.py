"""
Base schemas for common patterns.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseSchema):
    """Base response with ID and timestamps."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True


class PaginationParams(BaseSchema):
    """Pagination parameters."""
    page: int = 1
    per_page: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PaginatedResponse(BaseSchema):
    """Paginated response wrapper."""
    total: int
    page: int
    per_page: int
    total_pages: int


class MessageResponse(BaseSchema):
    """Simple message response."""
    message: str


class ErrorResponse(BaseSchema):
    """Error response."""
    detail: str
    type: Optional[str] = None
