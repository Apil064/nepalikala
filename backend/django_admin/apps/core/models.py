"""
Base model with common fields for all models.
"""
from django.db import models
import uuid


class BaseModel(models.Model):
    """Abstract base model with timestamp and soft delete."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        """Soft delete the instance."""
        self.is_active = False
        self.save()
