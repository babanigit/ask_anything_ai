from pathlib import Path

from dotenv import load_dotenv
import os

from corsheaders.defaults import default_headers

load_dotenv()  # 👈 this line is critical

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

OPENROUTER_URL = os.getenv("OPENROUTER_URL")
if not OPENROUTER_URL:
    raise RuntimeError("OPENROUTER_URL is not set")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
if not OPENROUTER_MODEL:
    raise RuntimeError("OPENROUTER_MODEL is not set")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

PRODUCTION_DOMAIN = os.getenv("PRODUCTION_DOMAIN")
if not PRODUCTION_DOMAIN:
    raise RuntimeError("PRODUCTION_DOMAIN is not set")

ENVIRONMENT = os.getenv("ENVIRONMENT")
if not ENVIRONMENT:
    raise RuntimeError("ENVIRONMENT is not set")
print(f"ENV ENVIRONMENT: {ENVIRONMENT}")

ENV_PERSONAL_DATA = os.getenv("ENV_PERSONAL_DATA")
if not ENV_PERSONAL_DATA:
    raise RuntimeError("ENV_PERSONAL_DATA is not set")

ENV_EXPERIENCE_DATA = os.getenv("ENV_EXPERIENCE_DATA")
if not ENV_EXPERIENCE_DATA:
    raise RuntimeError("ENV_EXPERIENCE_DATA is not set")

ENV_PROJECT_DATA = os.getenv("ENV_PROJECT_DATA")
if not ENV_PROJECT_DATA:
    raise RuntimeError("ENV_PROJECT_DATA is not set")

ENV_SKILLS_DATA = os.getenv("ENV_SKILLS_DATA")
if not ENV_SKILLS_DATA:
    raise RuntimeError("ENV_SKILLS_DATA is not set")

ENV_EDU_CERT_DATA = os.getenv("ENV_EDU_CERT_DATA")
if not ENV_EDU_CERT_DATA:
    raise RuntimeError("ENV_EDU_CERT_DATA is not set")

ENV_MODEL_LIST = os.getenv("ENV_MODEL_LIST")
if not ENV_MODEL_LIST:
    raise RuntimeError("ENV_MODEL_LIST is not set")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-xvrzr4c339ac=(=)r*^vwi+0=%dq&dll$q%@d%#*fr(jaljkd7'

# SECURITY WARNING: don't run with debug turned on in production!
# if ENVIRONMENT == "production":
#     DEBUG = False
# else:
#     DEBUG = True

# #  will look after this in production, but for development we can allow all hosts
ALLOWED_HOSTS = ["*"]
# if ENVIRONMENT == "production":
#     ALLOWED_HOSTS = [PRODUCTION_DOMAIN]
# else:
#     ALLOWED_HOSTS = ["*"]

# Application definition

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://ask-ai-flax.vercel.app",
# ]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-type',
    'authorization',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

INSTALLED_APPS = [
    'corsheaders',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'api',
    'ai',
    'personalPortfolio',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
