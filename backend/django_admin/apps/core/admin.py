"""
Core admin functionality.
"""
from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with common configurations."""
    list_per_page = 25
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        """Make created_at and updated_at read-only."""
        readonly = super().get_readonly_fields(request, obj)
        return list(readonly) + ['created_at', 'updated_at']
