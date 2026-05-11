from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.products.models import Product, Category
from apps.blog.models import BlogPost
from apps.seo.views import SEO_PAGES_DATA


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home', 'core:about', 'core:orders',
            'core:contact', 'blog:list',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Category.objects.filter(is_active=True)


class BlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class SEOPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return list(SEO_PAGES_DATA.keys())

    def location(self, item):
        return f'/{item}/'
