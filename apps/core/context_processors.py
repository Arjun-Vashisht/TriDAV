from django.conf import settings
from .models import SiteSettings


def site_settings(request):
    try:
        site = SiteSettings.objects.first()
    except Exception:
        site = None
    return {
        'site': site,
        'COMPANY_NAME': getattr(settings, 'COMPANY_NAME', 'TriDAV Impex'),
        'COMPANY_EMAIL': getattr(
            settings, 'COMPANY_EMAIL', 'tridavimpex@gmail.com'
        ),
        'COMPANY_PHONE': getattr(
            settings, 'COMPANY_PHONE', '+91-8979399684'
        ),
        'WHATSAPP_NUMBER': getattr(
            settings, 'WHATSAPP_NUMBER', '918979399684'
        ),
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
    }
