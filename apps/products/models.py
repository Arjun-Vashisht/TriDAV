from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(max_length=320, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Material(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    USAGE_CHOICES = [
        ('hotel', 'Hotel / Hospitality'),
        ('home', 'Home Use'),
        ('export', 'Orders / Wholesale'),
        ('all', 'All Uses'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    short_description = models.TextField(max_length=300, blank=True)
    description = models.TextField()
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    gsm = models.PositiveIntegerField(null=True, blank=True)
    thread_count = models.PositiveIntegerField(null=True, blank=True)
    size = models.CharField(max_length=100, blank=True)
    color_options = models.CharField(max_length=200, blank=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, default='all')
    moq = models.PositiveIntegerField(default=100)
    price_range = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(max_length=320, blank=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f'TRD-{slugify(self.name)[:10].upper()}'
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def related_products(self):
        return Product.objects.filter(
            category=self.category, is_active=True
        ).exclude(pk=self.pk)[:4]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} - Image {self.order}'


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=100)
    country_flag = models.CharField(max_length=10, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} - {self.company}'


class Certification(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='certifications/', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
