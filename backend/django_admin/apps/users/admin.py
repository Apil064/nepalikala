"""
User admin configuration.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, UserActivity


class UserResource(resources.ModelResource):
    """Import/Export resource for User model."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role',
                  'is_active', 'date_joined')


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    """Custom User Admin with role-based display."""
    resource_class = UserResource

    list_display = [
        'email', 'username', 'full_name', 'role_badge', 'is_active',
        'is_verified', 'date_joined', 'last_login'
    ]
    list_filter = ['role', 'is_active', 'is_verified', 'application_status', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio', 'location')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Artist Profile', {
            'fields': ('display_name', 'style', 'years_experience', 'portfolio_url',
                      'social_instagram', 'social_facebook', 'application_status'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

    readonly_fields = ['last_login', 'date_joined']

    def full_name(self, obj):
        """Display full name."""
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name or obj.username
    full_name.short_description = 'Name'

    def role_badge(self, obj):
        """Display role as colored badge."""
        colors = {
            'super_admin': '#8b1a1a',
            'admin': '#c8a84b',
            'editor': '#3a6fc4',
            'support': '#5c1a5c',
            'artist': '#2a7a50',
            'customer': '#6b6b6b',
        }
        color = colors.get(obj.role, '#6b6b6b')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    actions = ['make_active', 'make_inactive', 'approve_artists', 'verify_users']

    @admin.action(description='Mark selected users as active')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected users as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Approve selected artist applications')
    def approve_artists(self, request, queryset):
        queryset.filter(role='artist').update(application_status='approved')

    @admin.action(description='Verify selected users')
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for user activities."""
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'action', 'description']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 'timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
