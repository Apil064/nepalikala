"""
Order and cart endpoints.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.schemas.order import (
    CartResponse,
    CartItemBase,
    OrderResponse,
    OrderListResponse,
    OrderCreate,
    OrderUpdate,
    OrderFilterParams,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PaymentVerificationRequest,
    PartnershipEnquiryCreate
)

router = APIRouter()


# Cart endpoints
@router.get("/cart", response_model=CartResponse)
async def get_cart(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's shopping cart."""
    return {
        "items": [],
        "subtotal": 0,
        "shipping_estimate": None,
        "tax_estimate": None,
        "total_estimate": 0,
        "item_count": 0
    }


@router.post("/cart/items", status_code=201)
async def add_to_cart(
    item: CartItemBase,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add item to cart."""
    return {"message": "Item added to cart", "item_id": "mock-item-id"}


@router.patch("/cart/items/{item_id}")
async def update_cart_item(
    item_id: UUID,
    quantity: int = Query(..., ge=0),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update cart item quantity (0 to remove)."""
    return {"message": "Cart updated"}


@router.delete("/cart/items/{item_id}", status_code=204)
async def remove_from_cart(
    item_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove item from cart."""
    return None


@router.delete("/cart", status_code=204)
async def clear_cart(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Clear entire cart."""
    return None


# Order endpoints
@router.get("/", response_model=OrderListResponse)
async def list_orders(
    status: str = None,
    payment_status: str = None,
    start_date: str = None,
    end_date: str = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's orders."""
    return {
        "total": 0,
        "page": page,
        "per_page": per_page,
        "items": []
    }


@router.post("/checkout/session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    data: CheckoutSessionRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create checkout session (Khalti/eSewa integration)."""
    return {
        "session_id": "mock-session",
        "order_id": "mock-order-id",
        "order_number": "ORD-0001",
        "payment_url": "https://khalti.com/pay/mock",
        "amount": 85000,
        "currency": "NPR"
    }


@router.post("/checkout/verify")
async def verify_payment(
    data: PaymentVerificationRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify payment and complete order."""
    return {"message": "Payment verified", "order_id": data.order_id, "status": "paid"}


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get order by ID."""
    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new order (alternative to checkout flow)."""
    return {
        "id": "mock-order",
        "order_number": "ORD-0001",
        "customer_id": current_user.get("id"),
        "total": 85000,
        "status": "pending",
        "payment_status": "pending",
        "items": []
    }


# Partnership enquiries
@router.post("/partnerships", status_code=201)
async def create_partnership_enquiry(
    enquiry: PartnershipEnquiryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit partnership enquiry."""
    return {
        "message": "Partnership enquiry submitted",
        "enquiry_id": "mock-enquiry-id"
    }
