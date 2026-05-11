from .base import *  # noqa: F403
from decouple import config
import dj_database_url

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='').split(',')

# Railway provides DATABASE_URL automatically when PostgreSQL is added
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Railway terminates SSL at the proxy — tell Django to trust the forwarded header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway proxy handles this

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Cloudflare R2 for media uploads (product/category images)
# Set R2_* env vars in Railway dashboard to enable; falls back to local storage otherwise.
_r2_key = config('R2_ACCESS_KEY_ID', default='')
_r2_bucket = config('R2_BUCKET_NAME', default='')

if _r2_key and _r2_bucket:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = _r2_key
    AWS_SECRET_ACCESS_KEY = config('R2_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = _r2_bucket
    AWS_S3_ENDPOINT_URL = config('R2_ENDPOINT_URL')
    AWS_S3_CUSTOM_DOMAIN = config('R2_PUBLIC_DOMAIN', default='')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    _domain = AWS_S3_CUSTOM_DOMAIN or f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}'
    MEDIA_URL = f'https://{_domain}/'
