"""
Django settings for I-Architect orchestrator.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,orchestrator").split(",")

# ─────────────────────────────────────────────
# Application Definition
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "corsheaders",
    "rest_framework",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "api.middleware.quota_middleware.DiskQuotaMiddleware",
]

ROOT_URLCONF = "orchestrator.urls"

# ─────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "iarchitect"),
        "USER": os.environ.get("POSTGRES_USER", "iarchitect"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "iarchitect"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# ─────────────────────────────────────────────
# Redis
# ─────────────────────────────────────────────
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

# ─────────────────────────────────────────────
# Celery
# ─────────────────────────────────────────────
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# ─────────────────────────────────────────────
# External Services
# ─────────────────────────────────────────────
CHROMADB_URL = os.environ.get("CHROMADB_URL", "http://i-architect-chromadb:8000")
PLANTUML_URL = os.environ.get("PLANTUML_URL", "http://plantuml-server:8080")

# ─────────────────────────────────────────────
# Media / File Storage
# ─────────────────────────────────────────────
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))

# ─────────────────────────────────────────────
# REST Framework
# ─────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

# ─────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG

# ─────────────────────────────────────────────
# Project Limits
# ─────────────────────────────────────────────
PROJECT_DISK_QUOTA_MB = int(os.environ.get("PROJECT_DISK_QUOTA_MB", "500"))
PROJECT_MAX_VERSIONS = int(os.environ.get("PROJECT_MAX_VERSIONS", "5"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
