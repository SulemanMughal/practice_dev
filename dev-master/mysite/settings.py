import os
# ! PROJECT DIRECTORY
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9l$ef-y(q$3ixo*oziug4)z8y6#$vz9)#vh@ne^%-%wnd8z56i'
DEBUG = True
SEND = False
ALLOWED_HOSTS = ['localhost','167.172.128.142','127.0.0.1', 'www.circledin.io', "origin.circledin.io" , "3.209.205.115", "bs-local.com"]

# ------------------------------------------------------------------------------
# when you are going on Live
# Uncomment following "SITE_REDIRECT_ORIGINAL = https://joincircledin.com"
# Comment following  "SITE_REDIRECT_ORIGINAL = http://127.0.0.1:8000"
# And see  apps > templates > registration > password_reset_email > replace "http://127.0.0.1:8000" with the domain you like.

SITE_REDIRECT_ORIGINAL = "https://joincircledin.com"
# SITE_REDIRECT_ORIGINAL = "http://127.0.0.1:8000"
# -------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps', 
    'django.contrib.staticfiles',
    'apps',
    'django.contrib.humanize',
    'bootstrap_datepicker_plus',
    'django_social_share',
    'mathfilters',
    'blog',
    'ckeditor',
    'ckeditor_uploader'
]

SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'apps/templates'),
            os.path.join(BASE_DIR, 'blog/templates/blog'),
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                ''
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#      'ENGINE': 'django.db.backends.mysql',
#       'NAME': 'CircledIn_Db',
#        'USER': 'root',
#         'PASSWORD':'i;)LM;v$kFwHx$0T3X64G<.cKXgf)!Eu',
#         'HOST':'ls-ae48dd21c525115c6693356db343ed93aeb0cdb9.cn5zbpbn48n2.us-east-1.rds.amazonaws.com',
#         'PORT':'3306'

#   }
# }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
#--------------------------------------------------------------------------
from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
#--------------------------------------------------------------------------
#Email Setting...
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'joemontana9321@gmail.com'
EMAIL_HOST_PASSWORD = 'j23wgiNBge18'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Circledin"  
# SENDGRID_API_KEY = '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'

#-------------------------------------------------------------------------
#Media settings
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
SSTATICFILES_DIRS=[
    STATIC_ROOT,
    ]
MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR),'media')
#--------------------------------------------------------------------
#Authentication Backends...
AUTHENTICATION_BACKENDS=[
    'apps.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
#--------------------------------------------------------------------
# ! STRIPE API ID
STRIPE_SECRET_KEY = 'sk_test_jAndihGEFE8VtiRfUfTyygxH00JNgys3DY'
STRIPE_PUBLISHABLE_KEY = 'pk_test_7Caol5AeV11tgvLYCf7FlGXr00hMYbhIfm'
# ? Product List
PRODUCT_LIST_IDS=[
    'plan_HFv9CmBmgpSKED',
    'price_1H6NfSFx8Q0sUqQj5MZnPegV',
    'price_1H6NgPFx8Q0sUqQjx2RuaVzo',
    'price_1H6NhAFx8Q0sUqQjP7ygC99Z'
]
#--------------------------------------------------------------------
BOOTSTRAP4 = {
    'include_jquery': True,
}
#--------------------------------------------------------------------
# For session expire
SESSION_COOKIE_AGE = 30*60  # ! define number of second
#--------------------------------------------------------------------
# ? Google recaptcha
RECAPTCHA_SITE_KEY = "6LcqH74ZAAAAAOwKB7xcYtUVwMHaBlckxiHHTCOM"
RECAPTCHA_SECRET_KEY = "6LcqH74ZAAAAAIms-JWLR4Rzx8BuJC4Bvkko_5wM"
#--------------------------------------------------------------------
# ? Circledin Email ID
CIRCLEDIN_SUPPORT_EMAIL = "Support@Joincircledin.com"
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# ? Hubspot
HUBSPOT = "8273202.js"
#--------------------------------------------------------------------

# -------------------------------------------------------------------
# ? Google Analyst 
GOOGLE_ANALYST_SITE = "https://www.googletagmanager.com/gtag/js?id=G-0SP6Y09ZDY"
GOOGLE_ANALYST_SITE_ID = "G-0SP6Y09ZDY"
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# ? Calendly
CALENDLY_SITE = "https://assets.calendly.com/assets/external/widget.js"
CALENDLY_SITE_DATA_URL = "https://calendly.com/circledin?hide_landing_page_details=1&hide_gdpr_banner=1&primary_color=1dc9c2"
# -------------------------------------------------------------------

# CKEDITOR
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_BASEPATH = "/my_static/ckeditor/ckeditor/"
