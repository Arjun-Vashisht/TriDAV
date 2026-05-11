from django.contrib import admin
from .models import Category, Material, Product, ProductImage, Testimonial, Certification


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'usage', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'usage', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    inlines = [ProductImageInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'country', 'rating', 'is_active']
    list_editable = ['is_active']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
