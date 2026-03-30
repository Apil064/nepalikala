"""
Artworks admin configuration.
"""
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Artist, Artwork, ArtworkView, ArtistApplication


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Admin for art categories."""
    resource_class = CategoryResource
    list_display = ['name', 'slug', 'artwork_count', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}

    def artwork_count(self, obj):
        return obj.artworks.filter(is_active=True).count()
    artwork_count.short_description = 'Artworks'


class ArtistResource(resources.ModelResource):
    class Meta:
        model = Artist


@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    """Admin for artists."""
    resource_class = ArtistResource
    list_display = [
        'display_name', 'location', 'style', 'total_works',
        'total_sales', 'revenue_display', 'is_verified', 'is_featured'
    ]
    list_filter = ['is_verified', 'is_featured', 'style', 'location']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'bio']
    list_editable = ['is_verified', 'is_featured']
    readonly_fields = ['total_works', 'total_sales', 'revenue_npr', 'created_at', 'updated_at']

    fieldsets = (
        ('Profile', {
            'fields': ('user', 'bio', 'location', 'style', 'years_experience')
        }),
        ('Career', {
            'fields': ('education', 'awards', 'exhibitions')
        }),
        ('Online Presence', {
            'fields': ('website', 'instagram', 'facebook', 'twitter')
        }),
        ('Statistics', {
            'fields': ('total_works', 'total_sales', 'revenue_npr'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('portrait', 'cover_image')
        }),
        ('Settings', {
            'fields': ('is_verified', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def revenue_display(self, obj):
        return f"NPR {obj.revenue_npr:,.0f}"
    revenue_display.short_description = 'Revenue'

    actions = ['verify_artists', 'feature_artists', 'unfeature_artists']

    @admin.action(description='Mark selected artists as verified')
    def verify_artists(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description='Feature selected artists on homepage')
    def feature_artists(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='Remove selected from featured')
    def unfeature_artists(self, request, queryset):
        queryset.update(is_featured=False)


class ArtworkResource(resources.ModelResource):
    class Meta:
        model = Artwork


@admin.register(Artwork)
class ArtworkAdmin(ImportExportModelAdmin):
    """Admin for artworks."""
    resource_class = ArtworkResource
    list_display = [
        'title', 'artist_name', 'artwork_type', 'price_npr',
        'stock_display', 'status_badge', 'is_featured', 'view_count'
    ]
    list_filter = [
        'artwork_type', 'status', 'is_featured', 'is_new_arrival',
        'categories', 'year_created'
    ]
    search_fields = ['title', 'description', 'artist__user__first_name', 'artist__user__last_name']
    list_editable = ['artwork_type', 'is_featured']
    filter_horizontal = ['categories', 'additional_images']
    readonly_fields = ['view_count', 'total_sales', 'revenue_npr', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ['title']}

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'artist', 'categories', 'description')
        }),
        ('Artwork Details', {
            'fields': ('artwork_type', 'medium', 'dimensions', 'year_created')
        }),
        ('Pricing', {
            'fields': ('price_npr', 'price_usd')
        }),
        ('Print Edition', {
            'fields': ('edition_size', 'edition_number', 'prints_available'),
            'classes': ('collapse',),
            'description': 'Only applicable for prints'
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'is_new_arrival', 'is_active')
        }),
        ('Images', {
            'fields': ('main_image', 'additional_images')
        }),
        ('Statistics', {
            'fields': ('view_count', 'total_sales', 'revenue_npr'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def artist_name(self, obj):
        return obj.artist.display_name
    artist_name.short_description = 'Artist'

    def status_badge(self, obj):
        colors = {
            'available': '#2a7a50',
            'sold': '#6b6b6b',
            'reserved': '#c8a84b',
            'coming_soon': '#3a6fc4',
        }
        color = colors.get(obj.status, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = [
        'mark_available', 'mark_sold', 'mark_reserved',
        'feature_artworks', 'unfeature_artworks'
    ]

    @admin.action(description='Mark as available')
    def mark_available(self, request, queryset):
        queryset.update(status='available')

    @admin.action(description='Mark as sold')
    def mark_sold(self, request, queryset):
        queryset.update(status='sold')

    @admin.action(description='Mark as reserved')
    def mark_reserved(self, request, queryset):
        queryset.update(status='reserved')

    @admin.action(description='Feature selected artworks')
    def feature_artworks(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='Remove from featured')
    def unfeature_artworks(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(ArtworkView)
class ArtworkViewAdmin(admin.ModelAdmin):
    """Admin for artwork views."""
    list_display = ['artwork', 'user', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['artwork__title', 'user__email']
    readonly_fields = ['artwork', 'user', 'ip_address', 'user_agent', 'timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ArtistApplication)
class ArtistApplicationAdmin(admin.ModelAdmin):
    """Admin for artist applications."""
    list_display = [
        'full_name', 'location', 'art_style', 'years_experience',
        'status_badge', 'created_at'
    ]
    list_filter = ['status', 'art_style', 'years_experience', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'portfolio_description']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']

    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'location')
        }),
        ('Art Background', {
            'fields': ('art_style', 'years_experience', 'portfolio_url', 'portfolio_description')
        }),
        ('Online Presence', {
            'fields': ('website', 'instagram', 'facebook')
        }),
        ('Documents', {
            'fields': ('cv_document', 'sample_images')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_notes', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#c8a84b',
            'approved': '#2a7a50',
            'rejected': '#8b1a1a',
        }
        color = colors.get(obj.status, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['approve_applications', 'reject_applications']

    @admin.action(description='Approve selected applications')
    def approve_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )

    @admin.action(description='Reject selected applications')
    def reject_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
