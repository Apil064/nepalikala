"""
Artworks models - Categories, Artists, and Artworks.
"""
from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User


class Category(BaseModel):
    """Art category (Thangka, Modern, Madhubani, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Artist(BaseModel):
    """Artist profile linked to a user account."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='artist_profile',
        limit_choices_to={'role': User.Role.ARTIST}
    )
    bio = models.TextField(help_text="Detailed artist biography")
    location = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True, help_text="Primary art style")
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    education = models.TextField(blank=True, help_text="Art education background")
    awards = models.TextField(blank=True, help_text="Notable awards and recognitions")
    exhibitions = models.TextField(blank=True, help_text="Major exhibitions")

    # Social links
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)

    # Portfolio stats (auto-updated)
    total_works = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    revenue_npr = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Profile images
    portrait = models.ImageField(upload_to='artists/portraits/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='artists/covers/', blank=True, null=True)

    # Verification status
    is_verified = models.BooleanField(default=False, help_text="Verified artist badge")
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")

    class Meta:
        ordering = ['-is_featured', '-total_sales', 'user__first_name']
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    def update_stats(self):
        """Update artist statistics."""
        works = self.artworks.filter(is_active=True)
        self.total_works = works.count()
        self.total_sales = works.aggregate(
            total=models.Sum('total_sales')
        )['total'] or 0
        self.revenue_npr = works.aggregate(
            total=models.Sum('revenue_npr')
        )['total'] or 0
        self.save()


class Artwork(BaseModel):
    """Artwork/product model."""

    class ArtworkType(models.TextChoices):
        ORIGINAL = 'original', 'Original'
        PRINT = 'print', 'Print'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        SOLD = 'sold', 'Sold'
        RESERVED = 'reserved', 'Reserved'
        COMING_SOON = 'coming_soon', 'Coming Soon'

    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='artworks'
    )
    categories = models.ManyToManyField(Category, related_name='artworks', blank=True)

    # Artwork details
    description = models.TextField()
    artwork_type = models.CharField(
        max_length=20,
        choices=ArtworkType.choices,
        default=ArtworkType.ORIGINAL
    )
    medium = models.CharField(max_length=100, help_text="e.g., Natural pigments on cotton")
    dimensions = models.CharField(max_length=50, help_text="e.g., 60×80 cm")
    year_created = models.PositiveIntegerField(null=True, blank=True)

    # Pricing
    price_npr = models.DecimalField(max_digits=12, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Print-specific fields
    edition_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total edition size for prints"
    )
    edition_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Specific edition number (e.g., '12/30')"
    )
    prints_available = models.PositiveIntegerField(
        default=0,
        help_text="Number of prints available (for prints only)"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    # Images
    main_image = models.ImageField(upload_to='artworks/main/')
    additional_images = models.ManyToManyField('media.Media', blank=True, related_name='artworks')

    # Stats
    view_count = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    revenue_npr = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Features
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'

    def __str__(self):
        return f"{self.title} by {self.artist.display_name}"

    @property
    def stock_display(self):
        """Display stock information."""
        if self.artwork_type == self.ArtworkType.ORIGINAL:
            return "1" if self.status == self.Status.AVAILABLE else "0"
        return f"{self.prints_available}/{self.edition_size}"

    @property
    def is_in_stock(self):
        """Check if artwork is available for purchase."""
        if self.artwork_type == self.ArtworkType.ORIGINAL:
            return self.status == self.Status.AVAILABLE
        return self.prints_available > 0


class ArtworkView(models.Model):
    """Track artwork views for analytics."""
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.artwork.title} viewed on {self.timestamp}"


class ArtistApplication(models.Model):
    """Applications from artists wanting to join the platform."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    # Applicant info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # Art background
    location = models.CharField(max_length=100)
    art_style = models.CharField(max_length=100, help_text="Primary art style")
    years_experience = models.PositiveIntegerField()
    portfolio_url = models.URLField(blank=True)
    portfolio_description = models.TextField(help_text="Description of your work")

    # Social/professional links
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)

    # Documents
    cv_document = models.FileField(upload_to='applications/cvs/', blank=True, null=True)
    sample_images = models.ManyToManyField('media.Media', blank=True, related_name='applications')

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Artist Application'
        verbose_name_plural = 'Artist Applications'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
