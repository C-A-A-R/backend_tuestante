from .base import *
import pymysql
from urllib.parse import quote
import os
from ftplib import FTP_TLS

pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS_DEPLOY', default=['localhost', '127.0.0.1', 'backend-tuestante.onrender.com', '*'])

CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        "https://tuestante.com",
        "https://www.tuestante.com",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5500",
    ]
)

CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if env('SERVICION_BD', default='layerbase') == 'layerbase':
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'tuestantedb',
                'USER': 'root',
                'PASSWORD': 'S3QPkL9wjjiboE7EYXG5iwPa',
                'HOST': 'cloud.layerbase.dev',
                'PORT': '20415',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('MYSQL_DATABASE', default='nombre_base'),
            'USER': env('MYSQL_USER', default='usuario'),
        'PASSWORD': env('MYSQL_PASSWORD', default='contraseña'),
        'HOST': env('MYSQL_HOST', default='localhost'),
        'PORT': env('MYSQL_PORT', default='3306'),
    }
}

# --- Configuración de almacenamiento Multimedia vía FTP ---
# =========================================================
# FTPS
# =========================================================

FTP_USER = env("FTP_USER").strip()
FTP_PASSWORD = env("FTP_PASSWORD")
FTP_HOST = env("FTP_HOST").strip()
FTP_PORT = env("FTP_PORT", default="21").strip()


FTP_LOCATION = (
    f"ftps://"
    f"{FTP_USER}:"
    f"{FTP_PASSWORD}@"
    f"{FTP_HOST}:"
    f"{FTP_PORT}/"
)


# =========================================================
# MEDIA
# =========================================================

MEDIA_URL = env(
    "MEDIA_BASE_URL",
    default="https://imagenes-tu-estante.tuestante.com/"
)


# =========================================================
# STORAGE
# =========================================================

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.ftp.FTPStorage",
        "OPTIONS": {
            "location": FTP_LOCATION,
            "base_url": MEDIA_URL,
        },
    },

    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage."
            "StaticFilesStorage"
        ),
    },
}