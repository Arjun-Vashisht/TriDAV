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

## Production Deployment (100% free stack)

Render's own free Postgres database auto-deletes 30 days after creation (44
with the grace period), so this stack pairs Render's free web service with
Neon for a database that stays free indefinitely.

**1. Database — Neon (free Postgres, never expires)**
- Create an account at neon.tech and a new project (free tier: 0.5 GB storage,
  scales to zero when idle — plenty for a low-traffic B2B site).
- Copy the connection string it gives you (starts with `postgresql://...`).

**2. Media storage — Cloudflare R2 (optional but recommended)**
- Render's free web service has no persistent disk: anything uploaded via
  `/admin/` is lost the next time the instance restarts or redeploys (which
  happens often on the free tier due to idle spin-down).
- The seed product/category images are committed to git, so they survive
  fine without R2. But if you'll add new products through the admin after
  launch, set up an R2 bucket (10 GB free, no egress fees) so those uploads
  persist. `config/settings/production.py` already wires this up — create a
  bucket + API token in the Cloudflare dashboard and set the `R2_*` env vars
  below. Skip this step if you're fine editing products only via git.

**3. Web service — Render**
- Push this repo to GitHub, then create a new Web Service on render.com
  pointing at it — Render auto-detects `render.yaml`.
- In the service's Environment tab, set:
  - `DATABASE_URL` → the Neon connection string from step 1
  - `ALLOWED_HOSTS` → your actual `*.onrender.com` hostname (Render assigns
    this once the service is created; update from the `tridav.onrender.com`
    placeholder in `render.yaml`)
  - `CSRF_TRUSTED_ORIGINS` → `https://` + the same hostname
  - `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` → a Gmail address + app password
    (not your regular password — generate one at myaccount.google.com/apppasswords)
  - `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`,
    `R2_ENDPOINT_URL`, `R2_PUBLIC_DOMAIN` → only if using R2 from step 2
  - `SECRET_KEY` is auto-generated by `render.yaml`; leave it alone.
- Render runs `migrate` and `collectstatic` automatically on each deploy
  (see `render.yaml`).
- Create an admin user after the first deploy via Render's Shell tab:
  `python manage.py createsuperuser`.

**4. Keep it warm — UptimeRobot (free, avoids cold starts)**
- Render's free web service spins down after 15 min idle (~30–60s to wake
  back up), and Neon's compute scales to zero on its own idle timer too.
  Neither has a way to fully disable this on the free tier — that's what
  paid plans remove.
- To avoid visitors ever hitting a cold start, sign up free at
  uptimerobot.com and add an HTTP(s) monitor pointed at your Render URL
  (e.g. `https://tridav.onrender.com/`) checking every 5 minutes. Each ping
  loads a real page (which queries Neon), so it keeps both the web service
  and the database warm. This stays within Render's 750 free hours/month
  (24/7 ≈ 730 hours) — no cost, just an extra free account.
- This isn't a 100%-guaranteed zero cold start (a ping could land seconds
  after Render's own spin-down check), but in practice it keeps the site
  warm almost all the time.

---

## Tech Stack

- **Backend**: Django 5.0 + Python 3.10+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Styling**: Tailwind CSS (CDN) + Custom CSS
- **Templates**: Django Template Language
- **SEO**: django.contrib.sitemaps, custom schema markup
- **Static files**: WhiteNoise
