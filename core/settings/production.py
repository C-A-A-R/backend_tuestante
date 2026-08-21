from .base import *
import pymysql
import urllib.parse

pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS_DEPLOY', default=['localhost', '127.0.0.1'])

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
FTP_USER = urllib.parse.quote_plus(env('FTP_USER', default=''))
FTP_PASS = urllib.parse.quote_plus(env('FTP_PASSWORD', default=''))
FTP_HOST = env('FTP_HOST', default='localhost')
FTP_PORT = env('FTP_PORT', default='21')
MEDIA_URL = env('MEDIA_BASE_URL', default='https://media.tudominio.com/')

# django-storages (Django >= 4.2)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.ftp.FTPStorage",
        "OPTIONS": {
            "location": f"ftp://{FTP_USER}:{FTP_PASS}@{FTP_HOST}:{FTP_PORT}/",
            "base_url": MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Compatibilidad para Django <= 4.1 (si aplica a tu versión)
DEFAULT_FILE_STORAGE = "storages.backends.ftp.FTPStorage"
FTP_STORAGE_LOCATION = f"ftp://{FTP_USER}:{FTP_PASS}@{FTP_HOST}:{FTP_PORT}/"
