"""
Django settings for costanza project.
"""

from pathlib import Path
import environ
import os
import sys
from datetime import timedelta 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-p)c#+kt6$-rhjr=+#yhi&u=)vw111v^s-xxjkyswk#+ibn)x07'

DEBUG = True

ALLOWED_HOSTS = []

# --- CONFIGURAÇÃO DE AMBIENTE (.env) ---
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))


# Application definition
INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 

    # Third-Party Apps
    'rest_framework',
    'rest_framework_simplejwt', 
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders', 
    'djoser', 
    
    # Django-Allauth (Social Auth)
    'allauth',
    'allauth.account', # ⬅️ APLICAÇÃO (Correto)
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    # Your Apps
    'user',
    'friends',
    'events',
    'trilhas',
    'gamification',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # ⬅️ ADICIONADO AQUI, ONDE PERTENCE
    'allauth.account.middleware.AccountMiddleware', 

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# --- CORS (Comunicação com Next.js Frontend) ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    # Adicione aqui o domínio de produção do seu frontend (e.g., "https://costanza.com")
]
CORS_ALLOW_CREDENTIALS = True 


# --- CONFIGURAÇÃO DO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# --- CONFIGURAÇÃO DO SIMPLE_JWT ---
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',), 
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'SIGNING_KEY': SECRET_KEY, 
}


# --- CONFIGURAÇÃO DO DJOSER ---
DJOSER = {
    'USER_ID_FIELD': 'id',
    'LOGIN_FIELD': 'email', 
    'TOKEN_MODEL': None, 

    'SERIALIZERS': {
        'user_create': 'user.serializers.CustomUserCreateSerializer', 
        'user': 'user.serializers.CustomUserSerializer',
        'current_user': 'user.serializers.CustomUserSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    
    'PASSWORD_RESET_CONFIRM_URL': 'http://localhost:3000/auth/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'http://localhost:3000/auth/username/reset/confirm/{uid}/{token}',
    'SOCIAL_AUTH_ALLOWED_REDIRECTS': ['http://localhost:3000', 'https://seusite.com'],
}


# --- CONFIGURAÇÃO DO ALLAUTH (Social Auth) ---
SITE_ID = 1 
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_URL = 'http://localhost:3000/auth/login' 


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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'OPTIONS': {'sslmode': 'require'}, 
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
AUTH_USER_MODEL = 'user.CustomUser'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static and Media files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'