"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8r)llp=vg+6r4#!k5jt!9e!)zblu$7n2+zlth3ovm#p5ytm^1-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost',"RohitMaurya14.pythonanywhere.com","103.206.101.254"]


AUTH_USER_MODEL='blog.User'
# Application definition
SIMPLE_JWT = {
    'ALGORITHM': 'HS256',  
    # 'SIGNING_KEY': '',  # This is the security key used to sign the JWT
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), 
    'ROTATE_REFRESH_TOKENS': False,  
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_FIELD': 'email'  
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'django.contrib.sites',
        'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',"http://103.206.101.254:5017"]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    #     'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',  
    # ],
    
}


CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',  
    'accep',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
     "allauth.account.middleware.AccountMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rohitmoriya8168@gmail.com'  # Replace with your Gmail address
EMAIL_HOST_PASSWORD = 'fgicgvjccwgaxcpx'  # Replace with your Gmail password or app password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ACCOUNT_AUTHENTICATION_METHOD = "email"  
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True 
LOGIN_URL = "/admin"    
ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',  
         'NAME': 'mydb',          
         'USER': 'root',             
         'PASSWORD': 'rootpassword',     
         'HOST': 'db',                   
         'PORT': '3306',                        # Default MySQL port
     }
 }



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "main/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR,'media')

SITE_ID = 1
LOCAL_HOST="http://103.206.101.254:8017/"


#import environ

#env =w;fgefhbeuyfex environ.Env()
#environ.Env.read_env()
#import dj_database_url
#DATABASES = {
 #   'default': dj_database_url.config(
  #      default=os.getenv('DATABASE_URL', 'mysql://RohitMaurya15:Rohit12345@@RohitMaurya15.mysql.pythonanywhere-services.com:3306/RohitMaurya15$default')
   # )
#}soi
