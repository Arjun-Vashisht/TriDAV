from django.shortcuts import render
from apps.products.models import Product
import markdown


SEO_PAGES_DATA = {
    'bedsheet-exporter-india': {
        'title': 'Bedsheet Supplier India – Bulk Bedsheets for Orders',
        'hero_title': 'Bulk Bedsheets for Orders',
        'hero_subtitle': 'Cotton-blend and microfibre bedsheets, available in standard sizes. Order-ready packaging. MOQ from 100 pieces.',
        'seo_title': 'Bedsheet Supplier India | Bulk Bedsheets | TriDAV Impex',
        'seo_description': 'TriDAV Impex: Bulk bedsheet supplier from India. Standard sizes, cotton-blend and microfibre options. Worldwide shipping.',
        'category_slug': 'bedsheets',
        'content_key': 'bedsheets',
    },
    'hotel-towel-supplier': {
        'title': 'Towel Supplier India – Bulk Bath Towels for Orders',
        'hero_title': 'Bulk Towels for Orders',
        'hero_subtitle': 'Absorbent bath towels, hand towels, and face towels. Available in standard GSM ranges. Order-ready.',
        'seo_title': 'Towel Supplier India | Bulk Bath Towels | TriDAV Impex',
        'seo_description': 'Bulk bath towels from India. Standard GSM options, plain colours, order-ready packaging. Request a quote from TriDAV Impex.',
        'category_slug': 'towels',
        'content_key': 'towels',
    },
    'bulk-comforter-manufacturer': {
        'title': 'Bulk Comforter Supplier India – Order Quality Bedding',
        'hero_title': 'Bulk Comforters for Orders',
        'hero_subtitle': 'Hollow-fibre and microfibre comforters in standard sizes. Lightweight and medium-weight options available.',
        'seo_title': 'Bulk Comforter Supplier India | Order Bedding | TriDAV Impex',
        'seo_description': 'TriDAV Impex supplies bulk comforters and bedding. Standard fill options, custom sizes available. Worldwide shipping.',
        'category_slug': 'comforters',
        'content_key': 'comforters',
    },
    'kitchen-towel-supplier': {
        'title': 'Kitchen Roll Supplier India – Bulk Kitchen Rolls & Tissue',
        'hero_title': 'Kitchen Rolls & Tissue Products for Orders',
        'hero_subtitle': 'Absorbent kitchen rolls and tissue products for household and food service use. Bulk supply available.',
        'seo_title': 'Kitchen Roll Supplier India | Bulk Tissue Products | TriDAV Impex',
        'seo_description': 'Bulk kitchen rolls and tissue products from India. Standard specifications, order-ready packaging. Enquire with TriDAV Impex.',
        'category_slug': 'kitchen-rolls',
        'content_key': 'kitchen_rolls',
    },
}

SEO_CONTENT = {
    'bedsheets': """
## Bulk Bedsheets for Domestic & International Buyers

TriDAV Impex supplies bedsheets to international buyers, distributors, and institutional clients. Our bedsheets are available in cotton-blend and microfibre fabrics to suit a range of end uses.

### Product Range
- **Percale Weave** – Crisp, lightweight, suitable for warm climates
- **Sateen Weave** – Smooth finish, suitable for hospitality use
- **Poly-Cotton Blend** – Durable, easy-care, cost-effective
- **Microfibre** – Wrinkle-resistant, soft handle

### Order Specifications

| Spec | Detail |
|------|--------|
| Material | Cotton-blend, Poly-Cotton, Microfibre |
| Sizes | Single, Double, Queen, King, Custom on request |
| MOQ | 100 pieces per design |
| Lead Time | Discussed at time of order |
| Packaging | Polybag or custom packaging on request |
""",
    'towels': """
## Bulk Towels for Orders

TriDAV Impex supplies bath towels, hand towels, and face towels to international buyers. Products are available in standard GSM ranges suited to residential and hospitality use.

### GSM Range
- **400 GSM** – Lightweight, quick-dry
- **500 GSM** – Standard weight, good absorbency
- **600 GSM** – Heavier weight, plush feel

### Available Options
- Plain colours
- Dobby border finish
- Custom label or embroidery on request

### MOQ: 100 pieces per SKU
""",
    'comforters': """
## Bulk Comforters for Orders

TriDAV Impex supplies comforters in standard and custom sizes with hollow-fibre or microfibre fill. Lightweight and medium-weight options are available.

### Fill Options
- **Hollow-Fibre Polyester** – Soft, washable, suitable for all climates
- **Microfibre Fill** – Lightweight warmth
- **Cotton Fill** – Natural, breathable

### Cover Fabrics
Percale, microfibre, brushed cotton. Standard sizes available.

### Sizes
Single, Double, Queen, King, Euro Square, custom on request
""",
    'kitchen_rolls': """
## Kitchen Rolls & Tissue Products for Orders

TriDAV Impex supplies kitchen rolls, tissue papers, and hygiene paper products for household and food service use.

### Product Range
- **Kitchen Rolls** – Perforated, absorbent, standard roll sizes
- **Tissue Papers** – Two-ply facial tissue, box and pouch format
- **Toilet Paper** – Two-ply and three-ply, standard roll and jumbo roll
- **Pocket Tissues** – Compact travel packs, individually sealed

### MOQ: 100 pieces per SKU
Custom packaging and private label available on request.
""",
}

SEO_STATS = [
    ('🌍', 'Worldwide'),
    ('100+', 'Min. Order Qty'),
    ('24h', 'Quote Response'),
]

SEO_CERTS = []

SEO_FAQS = [
    ('What is the minimum order quantity?', 'Our standard MOQ starts at 100 pieces per SKU for most products. Please enquire for specific product categories.'),
    ('Do you offer samples before bulk orders?', 'Yes. We encourage buyers to request samples before placing bulk orders. Please enquire for availability and timelines.'),
    ('Can you add our brand name or logo?', 'Custom label and packaging options are available for select product categories. Please share your requirements when enquiring.'),
    ('What are your payment terms?', 'Payment terms are discussed and agreed at the time of order.'),
    ('How long does production take?', 'Lead times are discussed based on order size and product. Please enquire for an accurate estimate.'),
]


def seo_landing(request, slug):
    page_data = SEO_PAGES_DATA.get(slug)
    if not page_data:
        from django.http import Http404
        raise Http404

    category = None
    if page_data.get('category_slug'):
        try:
            from apps.products.models import Category
            category = Category.objects.filter(slug=page_data['category_slug']).first()
        except Exception:
            pass

    products = []
    if category:
        products = Product.objects.filter(category=category, is_active=True)[:6]

    content_html = markdown.markdown(
        SEO_CONTENT.get(page_data['content_key'], ''),
        extensions=['tables', 'extra']
    )

    context = {
        **page_data,
        'slug': slug,
        'category': category,
        'products': products,
        'content_html': content_html,
        'all_seo_pages': list(SEO_PAGES_DATA.keys()),
        'seo_stats': SEO_STATS,
        'seo_certs': SEO_CERTS,
        'seo_faqs': SEO_FAQS,
        'meta_title': page_data['seo_title'],
        'meta_description': page_data['seo_description'],
    }
    return render(request, 'seo/landing.html', context)


def robots_txt(request):
    from django.http import HttpResponse
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /inquiry/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
