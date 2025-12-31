import os
from .settings import *

# Add Whitenoise middleware for static files
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database configuration for production
# For PostgreSQL on production platforms, you'll need to add dj-database-url to requirements.txt

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.environ.get('FORCE_HTTPS', 'False') == 'True'

# Session security
SESSION_COOKIE_SECURE = os.environ.get('FORCE_HTTPS', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('FORCE_HTTPS', 'False') == 'True'