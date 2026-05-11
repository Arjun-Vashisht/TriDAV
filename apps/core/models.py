from django.db import models


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=200, default='TriDAV Impex')
    tagline = models.CharField(max_length=300, blank=True)
    about_short = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    ga_tracking_id = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    years_experience = models.PositiveIntegerField(default=15)
    countries_served = models.PositiveIntegerField(default=30)
    products_count = models.PositiveIntegerField(default=500)
    clients_count = models.PositiveIntegerField(default=200)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.company_name
