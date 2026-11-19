
"""
Django settings for Silvia API.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Project paths and environment.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Security.
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False

# Allowed hosts.
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

PRODUCTION_ALLOWED_HOSTS = os.getenv("PRODUCTION_ALLOWED_HOSTS", "")

if PRODUCTION_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in PRODUCTION_ALLOWED_HOSTS.split(",")
        if host.strip()
    )

# Applications.
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    "corsheaders",
    'rest_framework',
    'silvia',
]

# Middleware.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "silvia.middleware.RequestBodyLimitMiddleware",
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Django REST Framework.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/min",
    },
}

# Internationalization.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files.
STATIC_URL = 'static/'

# Request size limits.
DATA_UPLOAD_MAX_MEMORY_SIZE = 4096

# CORS.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

PRODUCTION_FRONTEND_URL = os.getenv("PRODUCTION_FRONTEND_URL")

if PRODUCTION_FRONTEND_URL:
    CORS_ALLOWED_ORIGINS.append(PRODUCTION_FRONTEND_URL.rstrip("/"))
