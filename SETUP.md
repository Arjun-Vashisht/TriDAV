# TriDAV Impex – Setup Guide

## Quick Start (Development)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Seed sample data
python manage.py seed_data

# 7. Collect static files
python manage.py collectstatic

# 8. Start development server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin: http://127.0.0.1:8000/admin (use credentials from step 5)

---

## Project Structure

```
TriDAV/
├── config/                 # Django project settings
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── development.py  # Dev settings
│   │   └── production.py   # Prod settings (PostgreSQL, email)
│   └── urls.py             # Root URL config
│
├── apps/
│   ├── core/               # Homepage, About, Contact, Export pages
│   ├── products/           # Product catalog (Category, Product, Material)
│   ├── blog/               # Blog/SEO content engine
│   ├── inquiries/          # Bulk inquiry & contact forms
│   └── seo/                # SEO landing pages (/bedsheet-exporter-india etc.)
│
├── templates/              # HTML templates
│   ├── base.html           # Base layout (navbar, footer, meta, schema)
│   ├── partials/           # Reusable components
│   ├── core/               # Homepage, About, Contact, Export
│   ├── products/           # Category list, product detail, search
│   ├── blog/               # Blog list and detail
│   ├── inquiries/          # Bulk form, success pages
│   └── seo/                # SEO landing page template
│
├── static/
│   ├── css/main.css        # Custom CSS (animations, skeleton, reveal)
│   ├── js/main.js          # Interactions (navbar, lazy load, quick view)
│   └── images/             # Pattern SVG, logos, placeholders
│
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Key URLs

| Page | URL |
|------|-----|
| Homepage | `/` |
| About | `/about/` |
| Export Info | `/export/` |
| Contact | `/contact/` |
| Blog | `/blog/` |
| Bulk Inquiry | `/inquiry/bulk/` |
| Products (Category) | `/products/<slug>/` |
| Product Detail | `/products/<slug>/detail/` |
| Search | `/products/search/?q=query` |
| **SEO: Bedsheet Exporter** | `/bedsheet-exporter-india/` |
| **SEO: Hotel Towels** | `/hotel-towel-supplier/` |
| **SEO: Comforter** | `/bulk-comforter-manufacturer/` |
| **SEO: Kitchen Towels** | `/kitchen-towel-supplier/` |
| Sitemap | `/sitemap.xml` |
| Robots | `/robots.txt` |
| Admin | `/admin/` |

---

## Adding Products via Admin

1. Login at `/admin/`
2. Go to **Products > Categories** — add/edit categories
3. Go to **Products > Materials** — add fabric types
4. Go to **Products > Products** — add products with images
5. Use **Products > Testimonials** to manage B2B testimonials

---

## SEO Configuration

Each product and category has SEO fields:
- `seo_title` — overrides `<title>` tag
- `seo_description` — meta description

The SEO landing pages (`/bedsheet-exporter-india/` etc.) are code-based in `apps/seo/views.py`.

---

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure PostgreSQL credentials in `.env`
3. Set `ALLOWED_HOSTS=yourdomain.com`
4. Configure email SMTP settings
5. Use `config.settings.production` as settings module
6. Run `python manage.py collectstatic`
7. Use Gunicorn + Nginx for serving

---

## Tech Stack

- **Backend**: Django 5.0 + Python 3.10+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Styling**: Tailwind CSS (CDN) + Custom CSS
- **Templates**: Django Template Language
- **SEO**: django.contrib.sitemaps, custom schema markup
- **Static files**: WhiteNoise
