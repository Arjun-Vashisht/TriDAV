from django import forms
from .models import BulkInquiry, ContactMessage


class BulkInquiryForm(forms.ModelForm):
    class Meta:
        model = BulkInquiry
        fields = [
            'full_name', 'email', 'phone', 'company', 'country', 'website',
            'product_category', 'product_name', 'quantity',
            'size_requirements', 'material_preference',
            'custom_branding', 'target_price', 'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@company.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 234 567 8900'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company or Hotel name'}),
            'country': forms.TextInput(attrs={'placeholder': 'USA, UAE, UK...'}),
            'product_category': forms.TextInput(attrs={'placeholder': 'Bedsheets, Towels...'}),
            'product_name': forms.TextInput(attrs={'placeholder': 'Specific product if known'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'e.g. 500 pieces'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us more about your requirements...'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 234 567 8900'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}),
        }
