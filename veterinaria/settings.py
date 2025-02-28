import os
import socket
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Detectar automáticamente si estamos en PythonAnywhere
IN_PYTHONANYWHERE = 'pythonanywhere' in socket.gethostname()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--=#xt1cb2_v^$wrt0mf#7j(r#u^gn$go=-9@h0x*c5)w892ngj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IN_PYTHONANYWHERE  # True en local, False en producción

ALLOWED_HOSTS = ['www.flebo.cl', 'flebo.cl', 'fleboadmin.pythonanywhere.com', '127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vetweb',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'veterinaria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'veterinaria.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if IN_PYTHONANYWHERE:
    # Configuración de base de datos para PythonAnywhere
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fleboadmin$fleboadmin',
            'USER': 'fleboadmin',
            'PASSWORD': 'Romi2297.',
            'HOST': 'fleboadmin.mysql.pythonanywhere-services.com',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Configuración de base de datos para desarrollo local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'flebovet_db',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de Email con Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contactoflebovet@gmail.com'
EMAIL_HOST_PASSWORD = 'demd phld awxk divi'
DEFAULT_FROM_EMAIL = 'contactoflebovet@gmail.com'

# Configuración para mimetypes
import mimetypes
mimetypes.add_type("text/css", ".css", True)

# Configuración de archivos estáticos y media según entorno
if IN_PYTHONANYWHERE:
    # Configuración para PythonAnywhere
    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/fleboadmin/flebovet/staticfiles'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # Configuración para desarrollo local
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'vetweb', 'static')
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración adicional
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF y CORS configuración
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://fleboadmin.pythonanywhere.com',
    'https://www.flebo.cl',
    'https://flebo.cl'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'