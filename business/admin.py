from django.contrib import admin
from .models import Category, Business
# Register your models here.


admin.site.register(Category)

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'is_verified', 'is_featured', 'is_active', 'created_at')
    list_filter = ('status', 'is_verified', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'owner__username', 'owner__email', 'tagline')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    # fieldsets = (
    #     (None, {
    #         'fields': ('owner', 'name', 'slug', 'tagline', 'description', 'category', 'business_type', 'established_year', 'working_hours')
    #     }),
    #     ('Verification & Status', {
    #         'fields': ('is_verified', 'is_featured', 'is_active', 'status')
    #     }),
    #     ('SEO & Search Boosting', {
    #         'fields': ('meta_title', 'meta_description', 'keywords')
    #     }),
    #     ('Timestamps', {
    #         'fields': ('created_at', 'updated_at')
    #     }),
    # )