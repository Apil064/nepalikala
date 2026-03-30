"""
Blog/Stories models for Nepaliकला.
"""
from django.db import models
from django.utils.text import slugify
from apps.core.models import BaseModel
from apps.users.models import User
from apps.artworks.models import Artist, Artwork


class BlogCategory(BaseModel):
    """Category for blog posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name


class BlogPost(BaseModel):
    """Blog post / Story model."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'Under Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=300, blank=True)
    excerpt = models.TextField(
        max_length=500,
        help_text="Brief summary for listings",
        blank=True
    )

    # Content
    content = models.TextField(help_text="Full article content (supports HTML/Markdown)")
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    gallery = models.ManyToManyField('media.Media', blank=True, related_name='blog_posts')

    # Categorization
    categories = models.ManyToManyField(BlogCategory, related_name='posts', blank=True)
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags"
    )

    # Author info
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    author_name_override = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use this if author is not a system user (e.g., 'Guest Writer')"
    )

    # Related content
    featured_artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_posts'
    )
    featured_artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_posts'
    )

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    # Publication
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True)

    # Engagement
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)

    # Features
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")
    is_premium = models.BooleanField(default=False, help_text="Members-only content")
    reading_time_minutes = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-is_featured', '-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + '...'
        super().save(*args, **kwargs)

    @property
    def display_author(self):
        if self.author_name_override:
            return self.author_name_override
        if self.author:
            return self.author.get_full_name() or self.author.username
        return "Nepaliकला Editorial"


class BlogComment(models.Model):
    """Comments on blog posts."""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='blog_comments'
    )
    author_name = models.CharField(max_length=100, blank=True)
    author_email = models.EmailField(blank=True)
    content = models.TextField()

    # Moderation
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    # Reply structure
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'

    def __str__(self):
        return f"Comment by {self.author_name or 'Anonymous'} on {self.post.title}"
