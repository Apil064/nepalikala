"""
Order and cart schemas.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel, Field
import uuid

from app.schemas.base import BaseResponseSchema
from app.schemas.artwork import ArtworkResponse, ArtistSummary


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class CartItemBase(BaseModel):
    """Base cart item schema."""
    artwork_id: uuid.UUID
    quantity: int = Field(1, ge=1)


class CartItemResponse(CartItemBase, BaseResponseSchema):
    """Cart item response."""
    artwork: ArtworkResponse
    subtotal: Decimal


class CartResponse(BaseModel):
    """Cart response."""
    items: List[CartItemResponse]
    subtotal: Decimal
    shipping_estimate: Optional[Decimal] = None
    tax_estimate: Optional[Decimal] = None
    total_estimate: Decimal
    item_count: int


class Address(BaseModel):
    """Address schema."""
    line1: str
    line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str = "NP"


class OrderItemResponse(BaseModel):
    """Order item response."""
    id: uuid.UUID
    artwork_title: str
    artwork_type: str
    artist_name: str
    artist: Optional[ArtistSummary] = None
    price: Decimal
    quantity: int
    total: Decimal
    certificate_number: Optional[str] = None


class OrderBase(BaseModel):
    """Base order schema."""
    shipping_address: Address
    customer_notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Order creation schema."""
    pass


class OrderResponse(OrderBase, BaseResponseSchema):
    """Order response."""
    order_number: str
    customer_id: Optional[uuid.UUID] = None
    customer_email: str
    customer_first_name: str
    customer_last_name: str
    customer_phone: str
    items: List[OrderItemResponse]
    subtotal: Decimal
    shipping_cost: Decimal
    tax_amount: Decimal
    total: Decimal
    currency: str = "NPR"
    status: OrderStatus
    payment_status: PaymentStatus
    tracking_number: Optional[str] = None
    payment_method: Optional[str] = None

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Paginated order list."""
    total: int
    page: int
    per_page: int
    total_pages: int
    items: List[OrderResponse]


class OrderUpdate(BaseModel):
    """Order update schema."""
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    tracking_number: Optional[str] = None
    shipping_notes: Optional[str] = None
    admin_notes: Optional[str] = None


class OrderFilterParams(BaseModel):
    """Order filter parameters."""
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    page: int = 1
    per_page: int = 20


class CheckoutSessionRequest(BaseModel):
    """Checkout session creation request."""
    shipping_address: Address
    customer_notes: Optional[str] = None
    payment_method: str = "khalti"


class CheckoutSessionResponse(BaseModel):
    """Checkout session response."""
    session_id: str
    order_id: uuid.UUID
    order_number: str
    payment_url: Optional[str] = None
    amount: Decimal
    currency: str = "NPR"


class PaymentVerificationRequest(BaseModel):
    """Payment verification request."""
    payment_id: str
    order_id: uuid.UUID


class PartnershipType(str, Enum):
    HOSPITALITY = "hospitality"
    CORPORATE = "corporate"
    GOVERNMENT = "government"
    NGO = "ngo"
    OTHER = "other"


class PartnershipEnquiryCreate(BaseModel):
    """Partnership enquiry creation."""
    organization: str
    contact_name: str
    contact_email: str
    contact_phone: Optional[str] = None
    partnership_type: PartnershipType
    budget_range: Optional[str] = None
    message: str


class PartnershipEnquiryResponse(PartnershipEnquiryCreate, BaseResponseSchema):
    """Partnership enquiry response."""
    status: str
