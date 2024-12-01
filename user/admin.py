from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # Adjust the import if needed

class UserAdmin(BaseUserAdmin):
    # Define the fields to be used in displaying the User model.
    list_display = ('mobile_number', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('mobile_number', 'first_name', 'last_name')
    ordering = ('mobile_number',)

    # Define the fieldsets
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'beetle_coin', 'premium_details', 'is_premium_member', 'premium_validity')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Define the add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    # Use custom UserAccountManager
    # add_form = UserCreationForm
    # form = UserChangeForm

# Register the custom User model and UserAdmin
admin.site.register(User, UserAdmin)
