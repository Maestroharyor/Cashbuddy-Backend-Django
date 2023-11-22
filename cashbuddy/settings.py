"""
Django settings for cashbuddy project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from django.core.management.commands.runserver import Command as runserver

load_dotenv()

# Content Security Policy

CSP_IMG_SRC = ("'self'")

CSP_STYLE_SRC = ("'self'")

CSP_SCRIPT_SRC = ("'self'")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6be8dekx7c_0tpll2+gh#9-dpsl-%i(1glw%n2a%90oe&^3(3t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')
print("Test: ",os.environ.get('DEBUG'))

# Define a custom port
PORT = 8010

runserver.default_port = f"{PORT}"

# Add the custom port to ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1', f'127.0.0.1:{PORT}', '.vercel.app', '.now.sh']

AUTH_USER_MODEL = 'cashbuddy.CustomUser'  # Change this to your custom user model
USER_ID_FIELD = 'user_id'  # Change this to the actual field in your user model

# Email Settings
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Use console backend for email during development
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'maestro@braandly.com'
EMAIL_HOST = 'smtp.dreamhost.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'maestro@braandly.com'
EMAIL_HOST_PASSWORD = 'By@maestAd2022!'



# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'rest_framework.authtoken',
    'cashbuddy',
];

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #  'rest_framework.authtoken.middleware.TokenMiddleware',
    'csp.middleware.CSPMiddleware'
]

ROOT_URLCONF = 'cashbuddy.urls'

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

WSGI_APPLICATION = 'cashbuddy.wsgi.app'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_simplejwt.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# if DEBUG:
#     REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
# else:
#     REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.JSONRenderer')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
'default': {
    'ENGINE': os.environ.get('DB_ENGINE'),
    'NAME': os.environ.get('CashBuddy'),
    'USER': os.environ.get('Maestroharyor'),
    'PASSWORD': os.environ.get('0lgu1GqPyVif'),
    'HOST': os.environ.get('ep-steep-cherry-68003624.us-east-2.aws.neon.tech'),
    'PORT': os.environ.get('5432'),
    'OPTIONS': {'sslmode': 'require'},
  }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
