"""
Blog admin configuration.
"""
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import BlogCategory, BlogPost, BlogComment


class BlogCommentInline(admin.TabularInline):
    """Inline for blog comments."""
    model = BlogComment
    extra = 0
    fields = ['author', 'author_name', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


class BlogPostResource(resources.ModelResource):
    class Meta:
        model = BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """Admin for blog categories."""
    list_display = ['name', 'slug', 'post_count', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}

    def post_count(self, obj):
        return obj.posts.filter(status='published').count()
    post_count.short_description = 'Published Posts'


@admin.register(BlogPost)
class BlogPostAdmin(ImportExportModelAdmin):
    """Admin for blog posts."""
    resource_class = BlogPostResource
    list_display = [
        'title', 'display_author', 'status_badge', 'is_featured',
        'view_count', 'published_at'
    ]
    list_filter = ['status', 'is_featured', 'is_premium', 'categories', 'published_at']
    search_fields = ['title', 'content', 'excerpt', 'author__email']
    list_editable = ['is_featured']
    filter_horizontal = ['categories', 'gallery']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'published_at'
    inlines = [BlogCommentInline]

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'subtitle', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery')
        }),
        ('Categorization', {
            'fields': ('categories', 'tags')
        }),
        ('Author', {
            'fields': ('author', 'author_name_override')
        }),
        ('Featured Content', {
            'fields': ('featured_artist', 'featured_artwork'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('status', 'published_at', 'is_featured', 'is_premium')
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count', 'share_count', 'reading_time_minutes'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'draft': '#6b6b6b',
            'review': '#c8a84b',
            'published': '#2a7a50',
            'archived': '#8b1a1a',
        }
        color = colors.get(obj.status, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['publish_posts', 'unpublish_posts', 'feature_posts']

    @admin.action(description='Publish selected posts')
    def publish_posts(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())

    @admin.action(description='Unpublish selected posts')
    def unpublish_posts(self, request, queryset):
        queryset.update(status='draft', published_at=None)

    @admin.action(description='Feature selected posts')
    def feature_posts(self, request, queryset):
        queryset.update(is_featured=True)


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    """Admin for blog comments."""
    list_display = ['post', 'author_name', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'created_at']
    search_fields = ['content', 'author_name', 'author_email', 'post__title']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

    actions = ['approve_comments', 'feature_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Feature selected comments')
    def feature_comments(self, request, queryset):
        queryset.update(is_featured=True)
