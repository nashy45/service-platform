from pathlib import Path
import os
try:
    from decouple import config
    import dj_database_url
    USE_PRODUCTION_SETTINGS = True
except ImportError:
    # For local development without production packages
    USE_PRODUCTION_SETTINGS = False
    def config(key, default=None, cast=None):
        return os.environ.get(key, default)

BASE_DIR = Path(__file__).resolve().parent.parent

if USE_PRODUCTION_SETTINGS:
    SECRET_KEY = config('SECRET_KEY', default='django-insecure-pai!+qw5(ue^lvgxfzdl_5z_(8&z%ch!e(86zb(*m_!0qp++a2')
    DEBUG = config('DEBUG', default=True, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
else:
    SECRET_KEY = 'django-insecure-pai!+qw5(ue^lvgxfzdl_5z_(8&z%ch!e(86zb(*m_!0qp++a2'
    DEBUG = True
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_tailwind',
    'channels',
    # Local apps
    'accounts',
    'services',
    'bookings',
    'payments',
    'reviews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'service_platform.urls'

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

WSGI_APPLICATION = 'service_platform.wsgi.application'
ASGI_APPLICATION = 'service_platform.asgi.application'

if USE_PRODUCTION_SETTINGS and 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

# Django Allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# Stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'your-stripe-public-key')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'your-stripe-secret-key')

# Cloudinary (optional)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# Email (console for dev)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Session & CSRF
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

if USE_PRODUCTION_SETTINGS:
    CSRF_TRUSTED_ORIGINS = config(
        'CSRF_TRUSTED_ORIGINS',
        default='http://127.0.0.1:8000,http://localhost:8000'
    ).split(',')
else:
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
