"""
Django settings for blog project.
MongoDB configuration for beginners workshop.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project — parent.parent resolves to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration - Using django-mongodb-backend
# This connects to MongoDB Atlas or local MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'HOST': os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/"),
        'ENFORCE_SCHEMA_IN_MIGRATIONS': False,
        'NAME': os.getenv("DB_NAME", 'test'),
        'COLLECTION_NAME': os.getenv("COLLECTION_NAME", 'posts'),
    }
}

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY", "your_api_key_here")

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'

# Silence MongoDB-specific system checks that are incompatible with contrib apps
SILENCED_SYSTEM_CHECKS = [
    "mongodb.E001",
    "mongodb.W001",
    "mongodb.W002",
    "mongodb.W003",
    "mongodb.W004",
    "mongodb.W005",
    "mongodb.W006",
]
