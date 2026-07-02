import re

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as serve_static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import (
    StaticViewSitemap, ProductSitemap, CategorySitemap,
    BlogSitemap, SEOPageSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
    'seo': SEOPageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('products/', include('apps.products.urls')),
    path('blog/', include('apps.blog.urls')),
    path('inquiry/', include('apps.inquiries.urls')),
    path('', include('apps.seo.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve /media/ locally whenever storage isn't an external backend (e.g. R2/S3).
# django.conf.urls.static.static() is a DEBUG-only no-op, so production needs
# its own route or the seed/uploaded images just 404 behind Whitenoise (which
# only ever covers STATIC_ROOT).
if settings.MEDIA_URL.startswith('/'):
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
            serve_static,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]

handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
