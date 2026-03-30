"""
Custom User model with role-based access control.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with roles for Nepaliकला."""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        EDITOR = 'editor', 'Editor'
        SUPPORT = 'support', 'Support'
        ARTIST = 'artist', 'Artist'
        CUSTOMER = 'customer', 'Customer'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    # Artist specific fields
    display_name = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True, help_text="Primary art style")
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    portfolio_url = models.URLField(blank=True)
    social_instagram = models.CharField(max_length=100, blank=True)
    social_facebook = models.CharField(max_length=100, blank=True)

    # Application status for artists
    application_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('not_applied', 'Not Applied'),
        ],
        default='not_applied'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_staff_member(self):
        """Check if user is any kind of staff."""
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ADMIN,
            self.Role.EDITOR,
            self.Role.SUPPORT
        ]

    @property
    def is_admin_user(self):
        """Check if user can access admin panel."""
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ADMIN
        ]

    @property
    def can_edit_content(self):
        """Check if user can edit content."""
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ADMIN,
            self.Role.EDITOR
        ]


class UserActivity(models.Model):
    """Track user activities for analytics."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.user.email} - {self.action}"
