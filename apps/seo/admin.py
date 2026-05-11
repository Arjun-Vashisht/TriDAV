from django.contrib import admin
from .models import SEOLandingPage, Country


@admin.register(SEOLandingPage)
class SEOLandingPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'flag_emoji', 'order', 'is_active']
    list_editable = ['order', 'is_active']
