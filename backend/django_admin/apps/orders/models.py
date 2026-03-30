"""
Orders and cart models.
"""
from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.artworks.models import Artwork


class CartItem(models.Model):
    """Shopping cart item."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'artwork']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity} x {self.artwork.title}"

    @property
    def subtotal(self):
        return self.artwork.price_npr * self.quantity


class Order(BaseModel):
    """Customer order."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    # Order identification
    order_number = models.CharField(max_length=50, unique=True)

    # Customer info
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    customer_email = models.EmailField()
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    # Shipping address
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)

    # Order totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='NPR')

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    # Shipping
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    shipping_notes = models.TextField(blank=True)

    # Payment
    payment_method = models.CharField(max_length=50, blank=True)
    payment_id = models.CharField(max_length=100, blank=True, help_text="Payment gateway transaction ID")
    paid_at = models.DateTimeField(null=True, blank=True)

    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)

    # IP and User Agent for fraud detection
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    """Individual item in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    artist = models.ForeignKey(
        'artworks.Artist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Snapshot of artwork data at time of purchase
    artwork_title = models.CharField(max_length=200)
    artwork_type = models.CharField(max_length=20)
    artist_name = models.CharField(max_length=200)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Artist revenue tracking
    artist_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Amount to be paid to artist"
    )
    platform_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Platform commission"
    )

    # License/certificate
    certificate_number = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity} x {self.artwork_title}"


class OrderStatusHistory(models.Model):
    """Track order status changes."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Order Status History'
        verbose_name_plural = 'Order Status Histories'

    def __str__(self):
        return f"{self.order.order_number}: {self.old_status} → {self.new_status}"


class PartnershipEnquiry(models.Model):
    """Partnership enquiries from businesses/organizations."""

    class Type(models.TextChoices):
        HOSPITALITY = 'hospitality', 'Hospitality'
        CORPORATE = 'corporate', 'Corporate'
        GOVERNMENT = 'government', 'Government'
        NGO = 'ngo', 'NGO/Cultural'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        ACTIVE = 'active', 'Active'
        DECLINED = 'declined', 'Declined'

    organization = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)

    partnership_type = models.CharField(
        max_length=20,
        choices=Type.choices
    )
    budget_range = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_partnerships'
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Partnership Enquiry'
        verbose_name_plural = 'Partnership Enquiries'

    def __str__(self):
        return f"{self.organization} - {self.status}"
