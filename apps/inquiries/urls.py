from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('bulk/', views.bulk_inquiry, name='bulk'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('success/', views.inquiry_success, name='success'),
    path('contact-success/', views.contact_success, name='contact_success'),
]
