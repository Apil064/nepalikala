"""
Media library models for Nepaliकला.
"""
import os
import uuid
from django.db import models
from django.utils.text import slugify


def generate_upload_path(instance, filename):
    """Generate upload path for media files."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"media/{instance.file_type}/{filename}"


class Media(models.Model):
    """Media file model for the media library."""

    class FileType(models.TextChoices):
        IMAGE = 'image', 'Image'
        DOCUMENT = 'document', 'Document'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        OTHER = 'other', 'Other'

    # File info
    file = models.FileField(upload_to=generate_upload_path)
    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        default=FileType.IMAGE
    )
    original_filename = models.CharField(max_length=255)

    # Metadata
    title = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Accessibility description")
    description = models.TextField(blank=True)

    # File details (auto-populated)
    file_size = models.PositiveBigIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)

    # Organization
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_media'
    )

    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Library'

    def __str__(self):
        return self.title or self.original_filename

    def save(self, *args, **kwargs):
        if not self.title and self.original_filename:
            name = os.path.splitext(self.original_filename)[0]
            self.title = name.replace('_', ' ').replace('-', ' ').title()
        super().save(*args, **kwargs)

    @property
    def dimensions(self):
        """Return dimensions string for images."""
        if self.width and self.height:
            return f"{self.width}×{self.height}"
        return None

    @property
    def file_size_formatted(self):
        """Return human-readable file size."""
        if not self.file_size:
            return "Unknown"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024
        return f"{self.file_size:.1f} TB"


class MediaFolder(models.Model):
    """Organizational folders for media library."""
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfolders'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'parent']
        ordering = ['name']
        verbose_name = 'Media Folder'
        verbose_name_plural = 'Media Folders'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
