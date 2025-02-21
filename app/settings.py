from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'matriculas',
    'materiais',
    
    'widget_tweaks',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'matriculas.middleware.VerificaAlteracaoSenhaMiddleware', 
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_USER_MODEL = 'matriculas.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SAMESITE = 'Lax'  # Define o atributo SameSite para o cookie de sessão
if os.getenv('DJANGO_ENV') == 'prod':
    SECURE_SSL_REDIRECT = True  # Redireciona todas as requisições HTTP para HTTPS
    SESSION_COOKIE_SECURE = True  # Garante que o cookie de sessão seja enviado apenas em conexões HTTPS
    CSRF_COOKIE_SECURE = True  # Garante que o cookie CSRF seja enviado apenas em conexões HTTPS
    SECURE_BROWSER_XSS_FILTER = True  # Ativa o filtro XSS do navegador
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Impede detecção MIME indevida
    X_FRAME_OPTIONS = 'DENY'  # Evita que o site seja carregado em iframes
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

JAZZMIN_SETTINGS = {
 # title of the window (Will default to current_admin_site.site_title if absent or None)
 'site_title': 'SVT',
 # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
 'site_header': 'SVT',
 # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
 'site_brand': 'SVT',
 "site_logo": "/img/logo.png",
 "login_logo": "/img/logo.png",
 'icons': {
 'auth': 'fas fa-users-cog',
 'auth.user': 'fas fa-user',
 'auth.Group': 'fas fa-users',
 'products.Brand': 'fas fa-copyright',
 'products.Category': 'fas fa-object-group',
 'products.Product': 'fas fa-box',
 },
 # Welcome text on the login screen
 'welcome_sign': 'Bem-vindo(a) ao SVT',
 # Copyright on the footer
 'copyright': 'VersatilTI LTDA',
 # List of model admins to search from the search bar, search bar omitted if excluded
 # If you want to use a single search field you dont need to use a list, you can use a simple string 
'search_model': ['matriculas.matricula',],
 # Whether to show the UI customizer on the sidebar
 'show_ui_builder': False,
 }
JAZZMIN_UI_TWEAKS = {
 'navbar_small_text': False,
 'footer_small_text': False,
 'body_small_text': False,
 'brand_small_text': False,
 'brand_colour': False,
 'accent': 'accent-primary',
 'navbar': 'navbar-white navbar-light',
 'no_navbar_border': False,
 'navbar_fixed': False,
 'layout_boxed': False,
 'footer_fixed': False,
 'sidebar_fixed': False,
 'sidebar': 'sidebar-dark-primary',
 'sidebar_nav_small_text': False,
 'sidebar_disable_expand': False,
 'sidebar_nav_child_indent': False,
 'sidebar_nav_compact_style': False,
 'sidebar_nav_legacy_style': False,
 'sidebar_nav_flat_style': False,
 'theme': 'minty',
 'dark_mode_theme': None,
 'button_classes': {
 'primary': 'btn-outline-primary',
 'secondary': 'btn-outline-secondary',
 'info': 'btn-info',
 'warning': 'btn-warning',
 'danger': 'btn-danger',
 'success': 'btn-success'
 }
}