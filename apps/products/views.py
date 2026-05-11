from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Material


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)

    # Filters
    material = request.GET.get('material')
    usage = request.GET.get('usage')
    sort = request.GET.get('sort', '-created_at')

    if material:
        products = products.filter(material__slug=material)
    if usage:
        products = products.filter(usage=usage)

    products = products.order_by(sort)

    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get('page', 1))

    base_qs = Product.objects.filter(category=category, is_active=True)
    active_material_slugs = base_qs.filter(
        material__isnull=False
    ).values_list('material__slug', flat=True).distinct()
    active_usage_values = base_qs.values_list('usage', flat=True).distinct()

    context = {
        'category': category,
        'products': page,
        'materials': Material.objects.filter(slug__in=active_material_slugs),
        'usage_choices': [
            (v, l) for v, l in Product.USAGE_CHOICES
            if v in active_usage_values and v != 'all'
        ],
        'active_filters': {'material': material, 'usage': usage, 'sort': sort},
        'meta_title': category.seo_title or f'{category.name} – TriDAV Impex',
        'meta_description': category.seo_description or f'Buy premium {category.name} in bulk from India. Order-ready products, competitive pricing.',
    }
    return render(request, 'products/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = product.related_products

    # Recommendation: same category, similar tags
    recommended = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).order_by('-is_featured')[:4]

    context = {
        'product': product,
        'related': related,
        'recommended': recommended,
        'meta_title': product.seo_title or f'{product.name} – TriDAV Impex',
        'meta_description': product.seo_description or product.short_description,
        'schema_product': True,
        'trust_signals': ['✓ ISO Certified Quality', '✓ Custom Branding Available', '✓ Worldwide Shipping', '✓ MOQ Flexible'],
    }
    return render(request, 'products/detail.html', context)


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    context = {
        'products': page,
        'query': query,
        'meta_title': f'Search: {query} – TriDAV Impex',
        'meta_description': f'Search results for {query} on TriDAV Impex.',
    }
    return render(request, 'products/search.html', context)


def quick_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    data = {
        'name': product.name,
        'short_description': product.short_description,
        'material': str(product.material) if product.material else '',
        'gsm': product.gsm,
        'thread_count': product.thread_count,
        'size': product.size,
        'moq': product.moq,
        'price_range': product.price_range,
        'url': product.get_absolute_url(),
    }
    return JsonResponse(data)
