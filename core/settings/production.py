from .base import *
import pymysql
from urllib.parse import quote
import os
from ftplib import FTP_TLS

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


host = os.environ["FTP_HOST"]
port = int(os.environ.get("FTP_PORT", "21"))
user = os.environ["FTP_USER"]
password = os.environ["FTP_PASSWORD"]

ftp = FTP_TLS()

print("Conectando...")
ftp.connect(host, port, timeout=15)

print("Conexión TCP establecida")

ftp.login(user, password)

print("Login correcto")

ftp.prot_p()

print("Canal de datos TLS protegido")

print("Directorio actual:")
print(ftp.pwd())

ftp.quit()

print("Conexión cerrada")

# =========================================================
# MEDIA
# =========================================================

MEDIA_URL = env(
    "MEDIA_BASE_URL",
    default="https://imagenes-tu-estante.tuestante.com/"
)



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