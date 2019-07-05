"""
Django settings for xfz project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c1f+8zlh*&5p02zu2!d#-5q$nj5x#%gg8l1fb^7nr6n)b+vfm*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.164.128']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'apps.news',
    'apps.cms',
    'apps.xfzauth',
    'apps.ueditor',
    'apps.course',
    'apps.payinfo',
    'rest_framework',
    'debug_toolbar',
]

MIDDLEWARE = [
    # debug_toolbar中间件；
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xfz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 修改templates的路径；
        'DIRS': [os.path.join(BASE_DIR, 'front','templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 配置模板的static标签；
            'builtins': [
                'django.templatetags.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'xfz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xfz',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


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

AUTH_USER_MODEL = 'xfzauth.User'

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# 静态文件存放路径；
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'front','dist'),
]

# 上传文件保存的路径；
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Qiniu配置
QINIU_ACCESS_KEY = 'GjdN0XJxtrLbINSxx4ZjXXitk7Aux5h046x9viB8'
QINIU_SECRET_KEY = '8ULlOQezsKZIRFl_Bie09GZIJyonH50aJH6RONhu'
QINIU_BUCKET_NAME = 'qmspace'
QINIU_DOMAIN = 'http://ps96zui1h.bkt.clouddn.com/'

# UEditor配置，七牛和自己的服务器，最少要配置一个；
# 七牛服务器配置；
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN

# 自己服务器配置；
UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR,'front','dist','ueditor','config.json')

# 一次加载多少篇文章
ONE_PAGE_NEWS_COUNT = 2

# Django-Debug-Toolbar相关的配置；
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_PANELS = [
    # 代表是哪个django版本
    # 'debug_toolbar.panels.versions.VersionsPanel',
    # 用来计时的，判断加载当前页面总共花的时间
    'debug_toolbar.panels.timer.TimerPanel',
    # 读取django中的配置信息
    # 'debug_toolbar.panels.settings.SettingsPanel',
    # 看到当前请求头和响应头信息
    # 'debug_toolbar.panels.headers.HeadersPanel',
    # 当前请求的想信息（视图函数，Cookie信息，Session信息等）
    # 'debug_toolbar.panels.request.RequestPanel',
    # 查看SQL语句
    'debug_toolbar.panels.sql.SQLPanel',
    # 静态文件
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 模板文件
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    # 缓存
    # 'debug_toolbar.panels.cache.CachePanel',
    # 信号
    # 'debug_toolbar.panels.signals.SignalsPanel',
    # 日志
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 重定向
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # 使用本地jQuery文件；
    'JQUERY_URL': ''
}

# 百度云的配置
# 控制台->用户中心->用户ID
BAIDU_CLOUD_USER_ID = 'e9e69a42d4d146a184fb5927e7fb8f5a'
# 点播VOD->全局设置->发布设置->安全设置->UserKey
BAIDU_CLOUD_USER_KEY = 'cce60dc28edd4f1a'

# 搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        # 设置haystack的搜索引擎
        'ENGINE': 'apps.news.whoosh_cn_backend.WhooshEngine',
        # 设置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 进行增、删、改的操作时，自动创建索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'