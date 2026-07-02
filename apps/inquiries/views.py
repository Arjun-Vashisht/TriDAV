from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import BulkInquiryForm, ContactForm
from .models import BulkInquiry


def bulk_inquiry(request):
    if request.method == 'POST':
        if request.POST.get('hp_contact_field'):
            return redirect('inquiries:success')
        form = BulkInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.source_page = request.META.get('HTTP_REFERER', '')
            inquiry.ip_address = request.META.get('REMOTE_ADDR')
            inquiry.save()
            try:
                send_mail(
                    f'New Bulk Inquiry from {inquiry.full_name} – {inquiry.company}',
                    f'Name: {inquiry.full_name}\nEmail: {inquiry.email}\nCountry: {inquiry.country}\nProduct: {inquiry.product_category}\nMessage: {inquiry.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.COMPANY_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Thank you! We will respond within 24 hours.')
            return redirect('inquiries:success')
    else:
        product_cat = request.GET.get('category', '')
        form = BulkInquiryForm(initial={'product_category': product_cat})

    context = {
        'form': form,
        'meta_title': 'Request Bulk Quote – TriDAV Impex',
        'meta_description': 'Get a custom bulk quote for premium Indian textiles. Bedsheets, towels, comforters for hotels and wholesalers.',
    }
    return render(request, 'inquiries/bulk_form.html', context)


def contact_submit(request):
    if request.method == 'POST':
        if request.POST.get('hp_contact_field'):
            return redirect('inquiries:contact_success')
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message received! We will get back to you shortly.')
            return redirect('inquiries:contact_success')
    return redirect('core:contact')


def inquiry_success(request):
    return render(request, 'inquiries/success.html', {
        'meta_title': 'Quote Request Sent – TriDAV Impex',
    })


def contact_success(request):
    return render(request, 'inquiries/contact_success.html', {
        'meta_title': 'Message Sent – TriDAV Impex',
    })
