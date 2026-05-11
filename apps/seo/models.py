from django.db import models
from django.urls import reverse


class SEOLandingPage(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    hero_title = models.CharField(max_length=300)
    hero_subtitle = models.TextField(max_length=500)
    hero_image = models.ImageField(upload_to='seo/heroes/', blank=True, null=True)
    content = models.TextField(help_text='Main body content (Markdown supported)')
    seo_title = models.CharField(max_length=200)
    seo_description = models.TextField(max_length=320)
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True)
    schema_type = models.CharField(max_length=50, default='Organization')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SEO Landing Page'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('seo:landing', kwargs={'slug': self.slug})


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
