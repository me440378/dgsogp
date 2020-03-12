import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%ebw&lr^y9$6kic^s^3c$*ufmti$s60+-2s8e*k(#8u2#&x0z@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #RESTful
    'rest_framework',
    #解决跨域
    'corsheaders',
    #定时任务
    'django_crontab',
    'backend.apps.BackendConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #解决跨域
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'dgsogp_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':['frontend/dist'],
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

# CORS 跨域白名单
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
# CORS 允许携带Cookie
# CORS_ALLOW_CREDENTIALS = True

# Add for vue.js
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist/static"),
]

WSGI_APPLICATION = 'dgsogp_django.wsgi.application'

# Crontab
CRONJOBS = [
    #定时测试任务
    ('*/1 * * * *', 'backend.cronjobs.testjob'),
    #从远端采集到本地再上传HDFS，创建Hadoopsources
    # ('0 0 * * *', 'backend.cronjobs.collectDataFromServers'),
    #将HDFS上的文件下载到本地，创建Metadata
    # ('0 0 * * *', 'backend.cronjobs.scanHadoopPutInDB'),
    #将HDFS上的文件下载到本地，根据Metadata入库
    # ('0 0 * * *', 'backend.cronjobs.scanHadoopTagMetadata'),
    #清空本地暂存目录
    # ('0 0 * * *', 'backend.cronjobs.freeLocalBaseDir'),
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'admin_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dgsogp_admin_db',
        'USER': 'dgsogp_admin',   #账户名
        'PASSWORD': '123456', #密码
        'HOST': '127.0.0.1', #主机
        'PORT': '3306', #端口
    },
    'data_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dgsogp_data_db',
        'USER': 'dgsogp_data',   #账户名
        'PASSWORD': '123456', #密码
        'HOST': '127.0.0.1', #主机
        'PORT': '3306', #端口
    },
}

DATABASE_ROUTERS = ['dgsogp_django.DatabaseAppsRouter.DatabaseAppsRouter']

DATABASE_APPS_MAPPING = {
    'sqlite3': 'default',
    'admin_db': 'admin_db',
    'data_db': 'data_db',
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                     '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file':{
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs/main.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs/main_debug.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'django_crontab': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_crontab.log'),
            'formatter': 'main_formatter',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_crontab.crontab': {
            'handlers': ['django_crontab'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Hong_Kong'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
