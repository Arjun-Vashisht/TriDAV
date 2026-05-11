from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed initial sample data for TriDAV Impex website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding TriDAV Impex data...\n')

        self._seed_site_settings()
        self._seed_materials()
        self._seed_categories()
        self._seed_products()
        self._seed_product_images()
        self._seed_certifications()
        self._seed_blog()
        self._seed_countries()
        self._seed_seo_pages()

        self.stdout.write(self.style.SUCCESS('\n✅ All data seeded successfully!'))
        self.stdout.write('👉 Run: python manage.py runserver')

    def _seed_site_settings(self):
        from apps.core.models import SiteSettings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                company_name='TriDAV Impex',
                tagline='Home Textiles & Hygiene Products for Bulk Orders',
                about_short=(
                    'TriDAV Impex supplies home textiles and hygiene products '
                    'to international buyers worldwide.'
                ),
                email='tridavimpex@gmail.com',
                phone='+91-8979399684',
                whatsapp='+918979399684',
                address='India',
                years_experience=0,
                countries_served=0,
                products_count=0,
                clients_count=0,
            )
            self.stdout.write('  ✓ Site settings created (update stats in admin)')

    def _seed_materials(self):
        from apps.products.models import Material
        materials = [
            ('100% Cotton', 'cotton',
             'Natural cotton fabric, breathable, soft, and highly absorbent'),
            ('Polyester', 'polyester',
             'Durable polyester fabric, wrinkle-resistant and easy-care'),
            ('Microfibre', 'microfibre',
             'Ultra-fine synthetic fibre, superior absorbency, lint-free, quick-dry'),
            ('Virgin Pulp', 'virgin-pulp',
             '100% virgin wood pulp, strong and hygienic'),
            ('Biodegradable Pulp', 'biodegradable-pulp',
             'Eco-friendly biodegradable pulp, soft and gentle'),
        ]
        for name, slug, desc in materials:
            Material.objects.get_or_create(
                slug=slug, defaults={'name': name, 'description': desc}
            )
        self.stdout.write('  ✓ Materials created')

    def _seed_categories(self):
        from apps.products.models import Category
        categories = [
            (
                'Bedsheets', 'bedsheets',
                'Cotton and polyester bedsheets for hotels and homes.',
                '🛏️', 1,
                'Bedsheet Supplier India – Bulk Bedsheets | TriDAV',
                'Bulk bedsheets from India. Cotton and polyester, hotel and home use, '
                'custom sizes available. Order-ready supply.',
            ),
            (
                'Towels', 'towels',
                'Cotton and microfibre towels for hotels, gyms, and households.',
                '🛁', 2,
                'Towel Supplier India – Bulk Bath Towels | TriDAV',
                'Cotton and microfibre bath towels from India. Hotel and home grade, '
                'bulk supply, ship worldwide.',
            ),
            (
                'Toilet Paper', 'toilet-paper',
                'Soft, strong, and hygienic toilet paper rolls in 2-ply variants.',
                '🧻', 3,
                'Toilet Paper Supplier India – Bulk Tissue Rolls | TriDAV',
                'Bulk toilet paper rolls from India. 2-ply, soft and strong, '
                'hygienic supply for hotels and institutions.',
            ),
            (
                'Kitchen Rolls', 'kitchen-rolls',
                'Multi-ply kitchen towel rolls for food-safe cleaning and absorption.',
                '🍽️', 4,
                'Kitchen Roll Supplier India – Bulk Kitchen Towels | TriDAV',
                'Bulk kitchen towel rolls from India. 4-ply, food-safe, '
                'superior wet strength, 100% virgin pulp.',
            ),
            (
                'Tissue Papers', 'tissue-papers',
                'Soft, biodegradable tissue papers for hygienic use.',
                '🌿', 5,
                'Tissue Paper Supplier India – Biodegradable Tissues | TriDAV',
                'Bulk tissue papers from India. Biodegradable, soft and gentle, '
                'highly absorbent, eco-friendly.',
            ),
            (
                'Pocket Tissues', 'pocket-tissues',
                'Compact, portable 2-ply pocket tissues for on-the-go use.',
                '📦', 6,
                'Pocket Tissue Supplier India – Bulk Pocket Tissues | TriDAV',
                'Bulk pocket tissues from India. 2-ply, soft, compact packaging '
                'for hospitality and retail use.',
            ),
        ]
        for name, slug, desc, icon, order, seo_title, seo_desc in categories:
            Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name, 'description': desc, 'icon': icon,
                    'order': order, 'seo_title': seo_title,
                    'seo_description': seo_desc,
                }
            )
        self.stdout.write('  ✓ Categories created')

    def _seed_products(self):
        from apps.products.models import Product, Category, Material

        cotton = Material.objects.filter(slug='cotton').first()
        polyester = Material.objects.filter(slug='polyester').first()
        microfibre = Material.objects.filter(slug='microfibre').first()
        virgin_pulp = Material.objects.filter(slug='virgin-pulp').first()
        bio_pulp = Material.objects.filter(slug='biodegradable-pulp').first()

        bedsheets = Category.objects.filter(slug='bedsheets').first()
        towels = Category.objects.filter(slug='towels').first()
        toilet = Category.objects.filter(slug='toilet-paper').first()
        kitchen = Category.objects.filter(slug='kitchen-rolls').first()
        tissue = Category.objects.filter(slug='tissue-papers').first()
        pocket = Category.objects.filter(slug='pocket-tissues').first()

        # (name, slug, cat, mat, gsm, tc, size, colors,
        #  usage, moq, price, featured, bestseller, new, short_desc, desc)
        products_data = [
            # --- Bedsheets ---
            (
                '100% Cotton Bedsheet – White',
                'cotton-bedsheet-white',
                bedsheets, cotton, None, 200,
                '108"×108", Custom',
                'White',
                'all', 100, '', True, True, False,
                (
                    '100% cotton bedsheet in white. 200TC, size 108"×108". '
                    'Smooth finish, suitable for hotels and home use.'
                ),
                (
                    '100% cotton bedsheet with a 200 thread count. '
                    'Available in 108"×108" and custom sizes. '
                    'Smooth, durable weave. Pre-washed for reduced shrinkage. '
                    'Suitable for hotel rooms and home bedding. '
                    'Packaged for safe international transit.'
                ),
            ),
            (
                'Polyester Bedsheet – White',
                'polyester-bedsheet-white',
                bedsheets, polyester, None, 200,
                '108"×108", Custom',
                'White',
                'all', 100, '', False, False, False,
                (
                    'Polyester bedsheet in white. 200TC, size 108"×108". '
                    'Wrinkle-resistant and easy-care.'
                ),
                (
                    'Polyester bedsheet with a 200 thread count. '
                    'Available in 108"×108" and custom sizes. '
                    'Wrinkle-resistant and easy-care. '
                    'Suitable for budget hotels, guesthouses, and rental properties. '
                    'Packaged for bulk orders.'
                ),
            ),
            (
                'Polyester Bedsheet – Grey',
                'polyester-bedsheet-grey',
                bedsheets, polyester, None, 200,
                '108"×108", Custom',
                'Grey',
                'all', 100, '', False, False, True,
                (
                    'Polyester bedsheet in grey. 200TC, size 108"×108". '
                    'Wrinkle-resistant with a modern neutral tone.'
                ),
                (
                    'Polyester bedsheet with a 200 thread count in grey. '
                    'Available in 108"×108" and custom sizes. '
                    'Wrinkle-resistant and easy-care. '
                    'Works well in contemporary hotel and home interiors. '
                    'Packaged for bulk orders.'
                ),
            ),
            # --- Towels ---
            (
                '100% Cotton Bath Towel – White',
                'cotton-bath-towel-white',
                towels, cotton, None, None,
                '70×140cm, Custom',
                'White',
                'all', 100, '', True, True, False,
                (
                    '100% cotton bath towel in white. '
                    'Soft, absorbent, suitable for hotel and home use.'
                ),
                (
                    '100% cotton terry bath towel. '
                    'Absorbent, soft, and durable through repeated washing. '
                    'Standard size 70×140cm; custom dimensions available. '
                    'Suitable for hotels, guesthouses, and home use. '
                    'Packaged for bulk orders.'
                ),
            ),
            (
                '100% Cotton Bath Towel – Charcoal',
                'cotton-bath-towel-charcoal',
                towels, cotton, None, None,
                '70×140cm, Custom',
                'Charcoal',
                'all', 100, '', False, False, True,
                (
                    '100% cotton bath towel in charcoal. '
                    'Soft, absorbent, suited to modern hotel and home interiors.'
                ),
                (
                    '100% cotton terry bath towel in charcoal. '
                    'Same construction as the white variant. '
                    'Works well in contemporary interiors. '
                    'Standard size 70×140cm; custom dimensions available.'
                ),
            ),
            (
                'Micro Fibre Towel',
                'microfibre-towel',
                towels, microfibre, None, None,
                'Standard, Custom',
                'Green, Custom',
                'all', 200, '', False, False, True,
                (
                    'Microfibre towel. Superior absorbency, lint-free & '
                    'streak-free, machine washable.'
                ),
                (
                    'Made from ultra-fine microfibre. '
                    'Superior absorbency. Lint-free and streak-free. '
                    'Durable and long lasting. Soft and gentle on surfaces. '
                    'Machine washable. '
                    'Suitable for hotels, gyms, and cleaning applications.'
                ),
            ),
            # --- Toilet Paper ---
            (
                'Toilet Paper – 2 Ply 15 GSM',
                'toilet-paper-2ply-15gsm',
                toilet, virgin_pulp, 15, None,
                'Standard Roll',
                'White',
                'all', 500, '', False, True, False,
                (
                    '2-ply toilet paper at 15 GSM. '
                    'Soft, strong, and hygienic.'
                ),
                (
                    '2-ply toilet paper at 15 GSM per ply. '
                    'Soft and strong, highly absorbent, and hygienic. '
                    'Suitable for hotel bathrooms, offices, and institutional use. '
                    'Available in bulk supply with order-ready packaging.'
                ),
            ),
            (
                'Toilet Paper – 2 Ply 17 GSM',
                'toilet-paper-2ply-17gsm',
                toilet, virgin_pulp, 17, None,
                'Standard Roll',
                'White',
                'all', 500, '', True, False, False,
                (
                    '2-ply toilet paper at 17 GSM. '
                    'Heavier weight for added softness and strength.'
                ),
                (
                    '2-ply toilet paper at 17 GSM per ply. '
                    'Heavier weight provides enhanced softness and strength. '
                    'Soft, highly absorbent, and hygienic. '
                    'Suitable for premium hotel and institutional use.'
                ),
            ),
            # --- Kitchen Rolls ---
            (
                'Premium Kitchen Towel Roll – 4 Ply',
                'premium-kitchen-towel-roll-4ply',
                kitchen, virgin_pulp, None, None,
                'Standard Roll',
                'White',
                'all', 300, '', True, True, False,
                (
                    '4-ply kitchen towel roll. 100% virgin pulp. '
                    'Food-safe, highly absorbent, superior wet strength.'
                ),
                (
                    '4-ply kitchen towel roll made from 100% virgin pulp. '
                    'Food-safe. Highly absorbent — quickly soaks up spills. '
                    'Superior wet strength: does not fall apart when wet. '
                    'Suitable for hotel kitchens, restaurants, and institutional use.'
                ),
            ),
            # --- Tissue Papers ---
            (
                'Biodegradable Tissue Paper – 1 Ply',
                'biodegradable-tissue-paper-1ply',
                tissue, bio_pulp, None, None,
                'Standard Sheet',
                'White',
                'all', 1000, '', False, False, True,
                (
                    'Biodegradable 1-ply tissue paper. '
                    'Eco-friendly, soft & gentle, highly absorbent.'
                ),
                (
                    'Biodegradable 1-ply tissue paper. '
                    'Biodegradable, soft and gentle on skin, highly absorbent, '
                    'strong and durable. Eco-friendly. '
                    'Suitable for hotels, wellness centres, and retail distribution.'
                ),
            ),
            # --- Pocket Tissues ---
            (
                '2 Ply Pocket Tissues',
                '2ply-pocket-tissues',
                pocket, virgin_pulp, None, None,
                'Pocket Pack',
                'White',
                'all', 1000, '', False, True, False,
                (
                    'Premium quality 2-ply pocket tissues. '
                    'Soft, portable, suitable for hotel amenities and retail.'
                ),
                (
                    '2-ply pocket tissues in compact packaging. '
                    'Soft and gentle. '
                    'Suitable for hotel in-room amenities, airline kits, '
                    'and retail distribution. '
                    'Available in plain and custom-branded packaging.'
                ),
            ),
        ]

        count = 0
        for row in products_data:
            (name, slug, cat, mat, gsm, tc, size, colors, usage, moq,
             price, featured, bestseller, new_arr, short_desc, desc) = row
            if cat and not Product.objects.filter(slug=slug).exists():
                Product.objects.create(
                    name=name, slug=slug, category=cat, material=mat,
                    gsm=gsm, thread_count=tc, size=size, color_options=colors,
                    usage=usage, moq=moq, price_range=price,
                    is_featured=featured, is_bestseller=bestseller, is_new=new_arr,
                    short_description=short_desc, description=desc,
                    sku=f'TRD-{slug[:45].upper()}',
                    seo_title=f'{name} – Bulk Orders | TriDAV',
                    seo_description=short_desc,
                )
                count += 1
        self.stdout.write(f'  ✓ {count} products created')

    def _seed_product_images(self):
        from apps.products.models import Product, ProductImage

        # slug → image filename in media/products/
        image_map = {
            'cotton-bedsheet-white':          'products/bedsheet-cotton-white.png',
            'polyester-bedsheet-white':        'products/bedsheet-polyester-white.png',
            'polyester-bedsheet-grey':         'products/bedsheet-polyester-grey.png',
            'cotton-bath-towel-white':         'products/towel-cotton-white.png',
            'cotton-bath-towel-charcoal':      'products/towel-cotton-charcoal.png',
            'microfibre-towel':                'products/towel-microfibre.png',
            'toilet-paper-2ply-15gsm':         'products/toilet-paper-15gsm.png',
            'toilet-paper-2ply-17gsm':         'products/toilet-paper-17gsm.png',
            'premium-kitchen-towel-roll-4ply': 'products/kitchen-roll-4ply.png',
            'biodegradable-tissue-paper-1ply': 'products/tissue-biodegradable.png',
            '2ply-pocket-tissues':             'products/pocket-tissues.png',
        }

        count = 0
        for slug, img_path in image_map.items():
            product = Product.objects.filter(slug=slug).first()
            if not product:
                continue
            if ProductImage.objects.filter(product=product).exists():
                continue
            ProductImage.objects.create(
                product=product,
                image=img_path,
                alt_text=product.name,
                is_primary=True,
                order=0,
            )
            count += 1
        self.stdout.write(f'  ✓ {count} product images linked')

    def _seed_certifications(self):
        from apps.products.models import Certification
        if Certification.objects.exists():
            return
        certs = [
            ('Pre-Shipment Inspection',
             'Products inspected against specifications before dispatch', 1),
            ('Order Documentation',
             'Full shipping and order documentation provided with every order', 2),
        ]
        for name, desc, order in certs:
            Certification.objects.create(name=name, description=desc, order=order)
        self.stdout.write('  ✓ Certifications created')

    def _seed_blog(self):
        from apps.blog.models import BlogPost, BlogCategory
        if BlogPost.objects.exists():
            return
        author = User.objects.filter(is_superuser=True).first()

        cat_buying, _ = BlogCategory.objects.get_or_create(
            slug='buying-guides', defaults={'name': 'Buying Guides'}
        )
        cat_orders, _ = BlogCategory.objects.get_or_create(
            slug='order-tips', defaults={'name': 'Order Tips'}
        )

        posts = [
            (
                'How to Choose the Right Bedsheets for Hotel Use',
                'choose-hotel-bedsheets-guide',
                cat_buying,
                (
                    'Selecting bedsheets for hotel use involves more than picking a '
                    'thread count. This guide covers the factors that affect '
                    'durability, guest comfort, and laundry performance.'
                ),
                '''## Choosing Bedsheets for Hotel and Hospitality Use

When buying bedsheets in bulk for hotels, the key factors are durability, comfort, and ease of laundering — not just aesthetics.

### Thread Count

Thread count (TC) measures the number of threads per square inch. A 200TC sheet is a practical standard for hotel use — durable, easy to launder, and comfortable.

### Material

**100% cotton** bedsheets are breathable and improve in softness with washing. They are the standard choice for mid-range and premium hotels.

**Polyester** bedsheets are wrinkle-resistant, easy-care, and a cost-effective option for budget hotels and rental properties.

### GSM (Grams per Square Metre)

GSM measures fabric weight. Heavier fabric generally means more durability but slower drying time:

| GSM Range | Typical Use |
|---|---|
| 90–110 GSM | Budget and lightweight |
| 120–150 GSM | Mid-range hotel standard |
| 150+ GSM | Durable institutional use |

### Shrinkage and Pre-Washing

Ask suppliers whether sheets are pre-washed before packing. Pre-washing reduces the shrinkage that occurs after the first few industrial washes. This matters for fitted sheet sizing.

### Sizing

Standard sizes vary between markets — US, UK, and EU dimensions differ. Confirm exact dimensions before ordering in bulk.

[Contact us to discuss your bedsheet requirements →](/inquiry/bulk/?category=Bedsheets)
''',
                False, 5,
            ),
            (
                'Cotton vs Microfibre Towels: A Practical Comparison',
                'cotton-vs-microfibre-towels',
                cat_buying,
                (
                    'Cotton and microfibre towels each have distinct properties. '
                    'Here is a practical comparison covering absorbency, '
                    'durability, drying time, and weight.'
                ),
                '''## Cotton vs Microfibre Towels

Both cotton and microfibre towels are widely used in hotels, gyms, and home settings. The right choice depends on your use case and priorities.

### Cotton Towels

Cotton terry is the traditional choice for bath towels. The looped pile construction absorbs water quickly and feels soft against skin. Cotton towels tend to improve in softness over the first several washes.

**Typical applications:** Hotel rooms, guesthouses, home bathrooms.

### Microfibre Towels

Microfibre is made from ultra-fine synthetic fibres. It absorbs moisture quickly and dries fast. Microfibre towels are lighter and more compact than cotton equivalents.

Key properties:
- Superior absorbency
- Lint-free and streak-free
- Durable and long lasting
- Machine washable
- Lightweight and compact

**Typical applications:** Gyms, sports facilities, housekeeping, cleaning.

### Comparison Summary

| Property | Cotton | Microfibre |
|---|---|---|
| Absorbency | High | High |
| Drying time | Slower | Fast |
| Softness | Soft, improves with washing | Soft, consistent |
| Weight | Heavier | Light |
| Lint | Some | None |
| Washing | Machine washable | Machine washable |

For hotel bathrooms where guest feel matters, cotton remains the standard choice. Microfibre is well-suited where quick turnaround and lightweight logistics are priorities.

[Get a bulk quote for towels →](/inquiry/bulk/?category=Towels)
''',
                True, 5,
            ),
            (
                'Understanding Paper Hygiene Products: GSM, Ply, and Pulp Quality',
                'understanding-paper-hygiene-products',
                cat_buying,
                (
                    'Toilet paper, kitchen rolls, and tissue papers are specified '
                    'by GSM, ply count, and pulp quality. Here is what each term '
                    'means and how it affects performance.'
                ),
                '''## Paper Hygiene Products: Key Specifications

When sourcing toilet paper, kitchen rolls, and tissue papers in bulk, the main specifications to understand are GSM, ply count, and pulp source.

### GSM (Grams per Square Metre)

GSM measures the weight of the paper:

- **Lower GSM (12–15):** Lightweight, standard use
- **Higher GSM (17–22):** Heavier, softer, more durable

Higher GSM generally means a thicker, softer product. For hotel use, 17 GSM 2-ply is a common specification.

### Ply Count

Ply refers to the number of paper layers:

- **1-ply:** Single layer — lower cost, used in tissue sheets
- **2-ply:** Two layers bonded together — standard for toilet tissue
- **4-ply:** Four layers — used in kitchen rolls for strength when wet

### Pulp Quality

**Virgin pulp** is made from fresh wood fibres. It produces whiter, stronger, more consistent paper. Used in most hotel-grade toilet paper and kitchen rolls.

**Biodegradable pulp** is processed to break down more readily. Used where environmental credentials are a priority.

### For Kitchen Rolls

Kitchen rolls need wet strength — the ability to hold together when soaked. A 4-ply structure from 100% virgin pulp provides this.

[Inquire about bulk paper hygiene products →](/inquiry/bulk/?category=Toilet+Paper)
''',
                False, 5,
            ),
            (
                'Order Documentation for Textile and Paper Products from India',
                'order-documentation-india-textiles',
                cat_orders,
                (
                    'An overview of the standard order documentation required '
                    'when importing home textiles and hygiene paper products from India.'
                ),
                '''## Order Documentation: What to Expect

When importing home textiles or hygiene paper products from India, the following documents are standard:

### Commercial Invoice

Issued by the seller. States buyer and seller details, product description, quantity, unit price, total value, and currency. Used for customs clearance in the destination country.

### Packing List

Lists each carton in the shipment: contents, gross weight, net weight, and dimensions. Required for customs inspection and warehouse receiving.

### Bill of Lading (Sea Freight) / Airway Bill (Air Freight)

The carrier's receipt confirming goods have been shipped. The Bill of Lading is also a document of title for sea shipments.

### Certificate of Origin

Confirms goods originated in India. Often required for customs duty calculation. Issued by designated bodies.

### Pre-Shipment Inspection Certificate

Where required, an inspection is conducted before goods are loaded. The certificate confirms goods match the order specification.

### Additional Documents (where applicable)

- **Test reports** (GSM, dimensions, strength — as specified by buyer)
- **Phytosanitary certificate** (for natural fibre products, some markets)

Confirm exact documentation requirements with your freight forwarder and customs broker before placing an order.

[Contact us to discuss order requirements →](/contact/)
''',
                False, 6,
            ),
        ]

        for title, slug, cat, excerpt, content, featured, read_time in posts:
            BlogPost.objects.create(
                title=title, slug=slug, author=author, category=cat,
                excerpt=excerpt, content=content, status='published',
                published_at=timezone.now(), is_featured=featured,
                read_time=read_time,
                seo_title=f'{title} | TriDAV Impex Blog',
                seo_description=excerpt[:320],
            )
        self.stdout.write('  ✓ Blog posts created')

    def _seed_countries(self):
        from apps.seo.models import Country
        if Country.objects.exists():
            return
        countries = [
            ('United States', '🇺🇸', 1), ('United Kingdom', '🇬🇧', 2),
            ('UAE', '🇦🇪', 3), ('Australia', '🇦🇺', 4), ('Canada', '🇨🇦', 5),
            ('Germany', '🇩🇪', 6), ('France', '🇫🇷', 7), ('Italy', '🇮🇹', 8),
            ('Japan', '🇯🇵', 9), ('Singapore', '🇸🇬', 10),
            ('Bahrain', '🇧🇭', 11), ('Qatar', '🇶🇦', 12), ('Kuwait', '🇰🇼', 13),
            ('South Africa', '🇿🇦', 14), ('New Zealand', '🇳🇿', 15),
            ('Netherlands', '🇳🇱', 16), ('Sweden', '🇸🇪', 17),
            ('Switzerland', '🇨🇭', 18), ('Spain', '🇪🇸', 19),
            ('Portugal', '🇵🇹', 20), ('Malaysia', '🇲🇾', 21),
            ('South Korea', '🇰🇷', 22), ('Turkey', '🇹🇷', 23),
            ('Brazil', '🇧🇷', 24), ('Mexico', '🇲🇽', 25), ('Norway', '🇳🇴', 26),
            ('Belgium', '🇧🇪', 27), ('Austria', '🇦🇹', 28),
            ('Chile', '🇨🇱', 29), ('Thailand', '🇹🇭', 30),
        ]
        for name, flag, order in countries:
            Country.objects.create(name=name, flag_emoji=flag, order=order)
        self.stdout.write('  ✓ Countries created')

    def _seed_seo_pages(self):
        self.stdout.write('  ✓ SEO landing pages are code-based (no DB needed)')
