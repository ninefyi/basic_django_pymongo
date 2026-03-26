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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.blog',         # Must be LAST so BlogConfig.ready() runs after AuthConfig.ready()
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files for Django admin and project assets.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'

# Custom User model that uses ObjectIdAutoField for MongoDB compatibility
AUTH_USER_MODEL = 'blog.User'

# Use cookie-based sessions to avoid MongoDB pk conflict in session saves
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

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
