from django.contrib import admin
from .models import BulkInquiry, ContactMessage


@admin.register(BulkInquiry)
class BulkInquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'country', 'product_category', 'status', 'created_at']
    list_filter = ['status', 'country', 'product_category']
    search_fields = ['full_name', 'email', 'company']
    list_editable = ['status']
    readonly_fields = ['created_at', 'ip_address']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_editable = ['is_read']
