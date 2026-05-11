from django.db import models


class BulkInquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('quoted', 'Quoted'),
        ('closed', 'Closed'),
    ]

    # Contact info
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    # Order details
    product_category = models.CharField(max_length=100, blank=True)
    product_name = models.CharField(max_length=200, blank=True)
    quantity = models.CharField(max_length=100, blank=True)
    size_requirements = models.CharField(max_length=200, blank=True)
    material_preference = models.CharField(max_length=200, blank=True)
    custom_branding = models.BooleanField(default=False)
    target_price = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source_page = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text='Internal notes')

    class Meta:
        verbose_name_plural = 'Bulk Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} – {self.company} ({self.created_at.strftime("%d %b %Y")})'


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} – {self.subject}'
