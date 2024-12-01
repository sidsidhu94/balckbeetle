from django.contrib import admin
from .models import Institute, Batch

# Register Institute model
@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')  # Display these fields in the admin list view
    search_fields = ('name', 'code')  # Add a search box to search by name or code

# Register Batch model
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'institute', 'batch_name', 'referral_code')  # Display these fields in the admin list view
    search_fields = ('batch_name', 'referral_code')  # Add search functionality for batches
    list_filter = ('institute',)  # Add a filter for institute on the right side
