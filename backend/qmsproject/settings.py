import os
from datetime import timedelta
from pathlib import Path

import environ
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')



SECRET_KEY = env('SECRET_KEY')


DEBUG = env('DEBUG')
#DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    "core",
    "accounts",
    "anagrafiche",
    "human_resources",
    "acquistopelli",
    "articoli",
    "manualeprocedure",
    "monitoraggi",
    "manutenzioni",
    "lwg",
    "autorizzazioni",
    "gestionerifiuti",
    "nonconformity",
    "chem_man",
    "antincendio",
    "ricette",
    "air_emissions",
    "lavorazioni",
    "vendite",
    
    "bootstrap5",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_countries",
    "django_filters",
    'widget_tweaks',
    'django.contrib.humanize',
    'django_seed',
    'debug_toolbar',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    
    
    
    
]

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyABpaqJWTsy7WGjWckbKcjYHJ3sk2AI-Hw'


CRISPY_TEMPLATE_PACK = "bootstrap5"
# La prossima variabile serve per fare in modo che Crispy avvisi in caso di errore
CRISPY_FAIL_SILENTLY = not DEBUG

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "debug_toolbar.middleware.DebugToolbarMiddleware",
  

]

ROOT_URLCONF = "qmsproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'),
                    os.path.join(BASE_DIR, 'accounts/templates'),
                    os.path.join(BASE_DIR, 'userprofile/templates'),
                    os.path.join(BASE_DIR, 'core/templates'),
                    os.path.join(BASE_DIR, 'human_resources/templates'),
                    os.path.join(BASE_DIR, 'acquistopelli/templates'),
                    os.path.join(BASE_DIR, 'articoli/templates'),
                    os.path.join(BASE_DIR, 'manualeprocedure/templates'),
                    os.path.join(BASE_DIR, 'monitoraggi/templates'),
                    os.path.join(BASE_DIR, 'manutenzioni/templates'),
                    os.path.join(BASE_DIR, 'lwg/templates'),
                    os.path.join(BASE_DIR, 'autorizzazioni/templates'),
                    os.path.join(BASE_DIR, 'gestionerifiuti/templates'),
                    os.path.join(BASE_DIR, 'nonconformity/templates'),
                    os.path.join(BASE_DIR, 'chem_man/templates'),
                    os.path.join(BASE_DIR, 'antincendio/templates'),
                    os.path.join(BASE_DIR, 'ricette/templates'),
                    os.path.join(BASE_DIR, 'air_emissions/templates'),
        ]
                ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "qmsproject.context_processors.nome_sito",
                "qmsproject.context_processors.logo_sito",
                "qmsproject.context_processors.fk_ward_records",
                'qmsproject.context_processors.app_icons',
            ],
        },
    },
]

WSGI_APPLICATION = "qmsproject.wsgi.application"

FIXTURES = [
    'autorizzazioni/fixtures/data.json',
    'manualeprocedure/fixtures/data.json',
    'acquistopelli/fixtures/tipoanimale.json',
    'acquistopelli/fixtures/tipogrezzo.json',
    'chem_man/fixtures/hazard.json',
    'chem_man/fixtures/precautionary.json',
    'chem_man/fixtures/simbologhs.json',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
#}

SQLITE_DB_PATH =  os.path.join(BASE_DIR, env('SQLITE_DB_PATH'))
if env('DATABASE_TYPE') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': SQLITE_DB_PATH,
        }
    }
elif env('DATABASE_TYPE') == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB_NAME'),
            'USER': env('POSTGRES_DB_USER'),
            'PASSWORD': env('POSTGRES_DB_PASSWORD'),
            'HOST': env('POSTGRES_DB_HOST'),
            'PORT': env('POSTGRES_DB_PORT'),
        }
    }
else:
    raise ValueError("Unknown database type specified in DATABASE_TYPE.")



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "it"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static'
    ]
#MEDIA_ROOT='/home/stefano/Documenti/dev/QMSProject/media-serve/'
#MEDIA_ROOT = os.path.join(BASE_DIR, '/media-serve')
#MEDIA_ROOT = '/home/django/media-serve/'

MEDIA_URL = '/media/'

# Imposta il percorso predefinito per STATIC_ROOT e MEDIA_ROOT
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_ROOT = env("MEDIA_ROOT")

# Verifica se DEBUG è True e sovrascrivi i percorsi se necessario
if not DEBUG:
    # Controlla se le variabili d'ambiente sono impostate per STATIC_ROOT e MEDIA_ROOT
    if env("STATIC_ROOT", default=None):
        STATIC_ROOT = env("STATIC_ROOT")
    if env("MEDIA_ROOT", default=None):
        MEDIA_ROOT = env("MEDIA_ROOT")


# Imposta il percorso del file di log di Django dal file .env
DJANGO_LOG_FILE = env('DJANGO_LOG_FILE')

# Configurazione dei log di Django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': DJANGO_LOG_FILE,  # Utilizza la variabile d'ambiente per il percorso del file di log
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


MESSAGE_TAGS = {
        messages.DEBUG: 'secondary',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
 }

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


CORS_ORIGIN_ALLOW_ALL = True


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}



SIMPLE_JWT.update({
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
})