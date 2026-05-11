from django.shortcuts import render
from apps.products.models import Category, Product, Certification
from apps.blog.models import BlogPost


WHY_CHOOSE_US = [
    (
        'Consistent Product Quality',
        'Each product is supplied to defined specifications, ensuring'
        ' uniform quality across all repeat orders.',
    ),
    (
        'Order-Ready Packaging',
        'Products are packaged for safe international transit with'
        ' appropriate labelling and standard documentation.',
    ),
    (
        'Flexible Order Quantities',
        'We accommodate small test orders as well as large container'
        ' loads, depending on the product category.',
    ),
    (
        'Broad Product Range',
        'From bedsheets and towels to tissue papers and kitchen rolls'
        ' — a wide selection of home and hygiene essentials.',
    ),
    (
        'Custom Branding Options',
        'Private label, custom colour, and packaging options are'
        ' available for select product categories.',
    ),
]

PROCESS_STEPS = [
    (
        '1',
        'Inquiry & Requirements',
        'Share your product requirements — category, quantity,'
        ' size specifications, and destination.',
    ),
    (
        '2',
        'Quotation & Samples',
        'We respond promptly with pricing, lead time, and sample'
        ' availability for your review.',
    ),
    (
        '3',
        'Order Confirmation',
        'Confirm specifications and quantities. Production begins'
        ' upon order confirmation.',
    ),
    (
        '4',
        'Quality Check & Dispatch',
        'Products are inspected before packing and dispatched with'
        ' full order documentation.',
    ),
]

QUALITY_TESTS = [
    'Weight and GSM Verification',
    'Dimensional Consistency Check',
    'Absorbency and Softness Assessment',
    'Stitching and Seam Integrity',
    'Colourfastness Testing',
    'Packaging Condition and Integrity',
    'Label Accuracy and Compliance',
    'Pre-Shipment Inspection',
]

DEFAULT_CERTIFICATIONS = []

ORDER_STEPS = [
    (
        '1',
        'Send Inquiry',
        'Share your product requirements — quantity,'
        ' specifications, and destination.',
    ),
    (
        '2',
        'Get Custom Quote',
        'We respond within 24 hours with pricing, lead time,'
        ' and a samples offer.',
    ),
    (
        '3',
        'Sample Approval',
        'Receive physical samples before placing the bulk order.',
    ),
    (
        '4',
        'Ship Worldwide',
        'We handle production, quality inspection, documentation,'
        ' and freight to your port.',
    ),
]

MOQ_TIERS = [
    (
        'Starter',
        '100 pcs per SKU',
        'Suitable for initial test orders. Mixed designs and colours'
        ' available on select products.',
        'bg-cream-50',
    ),
    (
        'Business',
        '500 pcs per SKU',
        'Preferred by wholesale distributors. Better unit pricing'
        ' and scheduled production slots.',
        'bg-white',
    ),
    (
        'Enterprise',
        '2000+ pcs per SKU',
        'Full container loads. Best unit pricing. Custom branding'
        ' and packaging options available.',
        'bg-sand-50',
    ),
]

SHIPPING_ITEMS = [
    'Incoterms: FOB / CIF as agreed',
    'Order documents: Commercial Invoice, Packing List,'
    ' Bill of Lading, Certificate of Origin',
    'Payment terms: As mutually agreed at time of order',
    'Lead time: Discussed based on order size and product',
    'Samples: Available on request before bulk orders',
]

CUSTOM_BRANDING = [
    (
        '🏷️',
        'Custom Labels',
        'Add your brand name or logo to product labels and packaging',
    ),
    (
        '🎨',
        'Custom Colours',
        'Available for select textile products with consistent'
        ' colour matching',
    ),
    (
        '📦',
        'Custom Packaging',
        'Branded polybags, boxes, and retail-ready packs on request',
    ),
]

DEFAULT_COUNTRIES = [
    '🇺🇸 USA', '🇬🇧 UK', '🇦🇪 UAE', '🇦🇺 Australia', '🇨🇦 Canada',
    '🇩🇪 Germany', '🇫🇷 France', '🇮🇹 Italy', '🇯🇵 Japan',
    '🇸🇬 Singapore', '🇧🇭 Bahrain', '🇶🇦 Qatar', '🇰🇼 Kuwait',
    '🇿🇦 South Africa', '🇳🇿 New Zealand', '🇸🇪 Sweden',
    '🇳🇴 Norway', '🇳🇱 Netherlands', '🇲🇾 Malaysia', '🇰🇷 South Korea',
]

TRUST_SIGNALS = [
    '✓ Consistent Quality Standards',
    '✓ Custom Branding Available',
    '✓ Worldwide Shipping',
    '✓ Flexible MOQ',
]


def home(request):
    masonry_images = [
        ('/media/products/bedsheet-cotton-white.png',    'Cotton Bedsheet White',     'h-48'),
        ('/media/products/towel-cotton-white.png',       'Cotton Towel White',        'h-64'),
        ('/media/products/toilet-paper-17gsm.png',       'Toilet Paper 17 GSM',       'h-56'),
        ('/media/products/bedsheet-polyester-grey.png',  'Polyester Bedsheet Grey',   'h-48'),
        ('/media/products/towel-microfibre.png',         'Microfibre Towel',          'h-72'),
        ('/media/products/toilet-paper-15gsm.png',       'Toilet Paper 15 GSM',       'h-48'),
        ('/media/products/kitchen-roll-4ply.png',        'Kitchen Towel Roll 4 Ply',  'h-56'),
        ('/media/products/towel-cotton-charcoal.png',    'Cotton Towel Charcoal',     'h-64'),
        ('/media/products/tissue-biodegradable.png',     'Biodegradable Tissue',      'h-48'),
        ('/media/products/pocket-tissues.png',           'Pocket Tissues',            'h-56'),
        ('/media/products/bedsheet-polyester-white.png', 'Polyester Bedsheet White',  'h-72'),
        ('/media/products/towel-cotton-white.png',       'Cotton Towel',              'h-48'),
    ]
    context = {
        'featured_categories': Category.objects.filter(
            is_active=True
        )[:6],
        'featured_products': Product.objects.filter(
            is_featured=True, is_active=True
        )[:8],
        'new_products': Product.objects.filter(
            is_new=True, is_active=True
        )[:4],
        'latest_posts': BlogPost.objects.filter(
            status='published'
        )[:3],
        'why_choose_us': WHY_CHOOSE_US,
        'trust_signals': TRUST_SIGNALS,
        'masonry_images': masonry_images,
        'meta_title': (
            'TriDAV Impex – Home Textiles & Hygiene Products for Bulk Orders'
        ),
        'meta_description': (
            'TriDAV Impex supplies bedsheets, comforters, towels,'
            ' doormats, toilet paper, kitchen rolls, tissue papers,'
            ' and pocket tissues for international buyers.'
        ),
    }
    return render(request, 'core/home.html', context)


def about(request):
    certifications = Certification.objects.all()
    context = {
        'certifications': certifications,
        'default_certifications': (
            DEFAULT_CERTIFICATIONS if not certifications else []
        ),
        'process_steps': PROCESS_STEPS,
        'quality_tests': QUALITY_TESTS,
        'stats': [],
        'founders': [
            ('Arjun Vashisht', 'AV'),
            ('Devanshu Jain', 'DJ'),
            ('Vishant Singh', 'VS'),
        ],
        'meta_title': (
            'About TriDAV Impex – Reliable Home & Hygiene Product Supplier'
        ),
        'meta_description': (
            'TriDAV Impex supplies quality home textiles and hygiene'
            ' paper products for international buyers.'
            ' Consistent quality, order-ready packaging.'
        ),
    }
    return render(request, 'core/about.html', context)


def orders_page(request):
    from apps.seo.models import Country
    countries = Country.objects.filter(is_active=True)
    context = {
        'countries': countries,
        'default_countries': DEFAULT_COUNTRIES if not countries else [],
        'order_steps': ORDER_STEPS,
        'moq_tiers': MOQ_TIERS,
        'shipping_items': SHIPPING_ITEMS,
        'custom_branding': CUSTOM_BRANDING,
        'meta_title': (
            'Bulk Orders – TriDAV Impex Home & Hygiene Products'
        ),
        'meta_description': (
            'Bulk orders for bedsheets, towels, tissue papers,'
            ' toilet paper, and more. MOQ from 100 pcs.'
            ' Worldwide shipping. Request a free quote.'
        ),
    }
    return render(request, 'core/orders.html', context)


def contact(request):
    context = {
        'meta_title': 'Contact TriDAV Impex – Bulk Product Inquiry',
        'meta_description': (
            'Contact TriDAV Impex for bulk orders of home textiles'
            ' and hygiene products. WhatsApp available.'
            ' We aim to respond within 24 hours.'
        ),
    }
    return render(request, 'core/contact.html', context)


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
