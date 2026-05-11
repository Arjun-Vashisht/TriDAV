from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import markdown


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField(max_length=400)
    content = models.TextField(help_text='Supports Markdown')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(max_length=320, blank=True)
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True)
    tags = TaggableManager(blank=True)
    read_time = models.PositiveIntegerField(default=5, help_text='Minutes to read')
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def content_html(self):
        return markdown.markdown(self.content, extensions=['extra', 'codehilite'])

    @property
    def effective_seo_title(self):
        return self.seo_title or self.title

    @property
    def effective_seo_description(self):
        return self.seo_description or self.excerpt
