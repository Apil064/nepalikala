"""
Orders admin configuration.
"""
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CartItem, Order, OrderItem, OrderStatusHistory, PartnershipEnquiry


class OrderItemInline(admin.TabularInline):
    """Inline for order items."""
    model = OrderItem
    extra = 0
    readonly_fields = ['artwork_title', 'artist_name', 'price', 'quantity', 'total', 'artist_revenue']
    fields = ['artwork_title', 'artist_name', 'price', 'quantity', 'total', 'artist_revenue']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class OrderStatusHistoryInline(admin.TabularInline):
    """Inline for order status history."""
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['old_status', 'new_status', 'changed_by', 'notes', 'timestamp']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    """Admin for orders."""
    resource_class = OrderResource
    list_display = [
        'order_number', 'customer_name', 'total_display', 'status_badge',
        'payment_status', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at', 'shipping_country']
    search_fields = ['order_number', 'customer_email', 'customer_first_name', 'customer_last_name']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'customer_email', 'customer_first_name', 'customer_last_name', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address_line1', 'shipping_address_line2', 'shipping_city',
                      'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total', 'currency')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Shipping', {
            'fields': ('tracking_number', 'shipped_at', 'delivered_at', 'shipping_notes'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_id', 'paid_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def customer_name(self, obj):
        return f"{obj.customer_first_name} {obj.customer_last_name}"
    customer_name.short_description = 'Customer'

    def total_display(self, obj):
        return f"{obj.currency} {obj.total:,.2f}"
    total_display.short_description = 'Total'

    def status_badge(self, obj):
        colors = {
            'pending': '#c8a84b',
            'processing': '#3a6fc4',
            'shipped': '#5c1a5c',
            'delivered': '#2a7a50',
            'cancelled': '#8b1a1a',
            'refunded': '#6b6b6b',
        }
        color = colors.get(obj.status, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = [
        'mark_processing', 'mark_shipped', 'mark_delivered',
        'mark_cancelled', 'mark_paid', 'export_csv'
    ]

    @admin.action(description='Mark as processing')
    def mark_processing(self, request, queryset):
        queryset.update(status='processing')

    @admin.action(description='Mark as shipped')
    def mark_shipped(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='shipped', shipped_at=timezone.now())

    @admin.action(description='Mark as delivered')
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())

    @admin.action(description='Mark as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')

    @admin.action(description='Mark as paid')
    def mark_paid(self, request, queryset):
        from django.utils import timezone
        queryset.update(payment_status='paid', paid_at=timezone.now())


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin for order items."""
    list_display = ['artwork_title', 'order', 'artist_name', 'price', 'quantity', 'total']
    list_filter = ['created_at']
    search_fields = ['artwork_title', 'artist_name', 'order__order_number']
    readonly_fields = ['artwork_title', 'artist_name', 'price', 'quantity', 'total', 'artist_revenue', 'platform_fee']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin for cart items."""
    list_display = ['user', 'artwork', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__email', 'artwork__title']


@admin.register(PartnershipEnquiry)
class PartnershipEnquiryAdmin(admin.ModelAdmin):
    """Admin for partnership enquiries."""
    list_display = ['organization', 'partnership_type', 'contact_name', 'status_badge', 'created_at']
    list_filter = ['status', 'partnership_type', 'created_at']
    search_fields = ['organization', 'contact_name', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Organization', {
            'fields': ('organization', 'partnership_type', 'message')
        }),
        ('Contact', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
        ('Budget', {
            'fields': ('budget_range',)
        }),
        ('Management', {
            'fields': ('status', 'assigned_to', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new': '#3a6fc4',
            'in_progress': '#c8a84b',
            'active': '#2a7a50',
            'declined': '#8b1a1a',
        }
        color = colors.get(obj.status, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_in_progress', 'mark_active', 'mark_declined']

    @admin.action(description='Mark as in progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='Mark as active')
    def mark_active(self, request, queryset):
        queryset.update(status='active')

    @admin.action(description='Mark as declined')
    def mark_declined(self, request, queryset):
        queryset.update(status='declined')
