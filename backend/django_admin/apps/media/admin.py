"""
Media admin configuration.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Media, MediaFolder


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Admin for media files."""
    list_display = ['thumbnail', 'title', 'file_type', 'dimensions', 'file_size_formatted', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['title', 'original_filename', 'tags']
    readonly_fields = ['file_size', 'width', 'height', 'mime_type', 'usage_count', 'created_at', 'updated_at']

    fieldsets = (
        ('File', {
            'fields': ('file', 'file_type', 'original_filename')
        }),
        ('Metadata', {
            'fields': ('title', 'alt_text', 'description', 'tags')
        }),
        ('Details', {
            'fields': ('file_size', 'width', 'height', 'mime_type'),
            'classes': ('collapse',)
        }),
        ('Usage', {
            'fields': ('usage_count', 'uploaded_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        """Display thumbnail preview for images."""
        if obj.file_type == 'image':
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.file.url if obj.file else ''
            )
        return format_html('<span>{}</span>', obj.file_type)
    thumbnail.short_description = 'Preview'

    def dimensions(self, obj):
        return obj.dimensions or '-'
    dimensions.short_description = 'Dimensions'


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    """Admin for media folders."""
    list_display = ['name', 'parent', 'description', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
