import os
from django.conf import settings

def configure_django():
    """Configura Django si no está configurado"""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='mi-clave-secreta-super-segura',
            ALLOWED_HOSTS=['*'],
            ROOT_URLCONF='config.urls',
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ['app/views/templates'],
                'APP_DIRS': False,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                    ],
                },
            }],
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': os.getenv('DB_DATABASE', 'pablogarciajcbd'),
                    'USER': os.getenv('MYSQL_USER', 'pablogarciajcuser'),
                    'PASSWORD': os.getenv('MYSQL_PASSWORD', 'password'),
                    'HOST': 'mysql',
                    'PORT': '3306',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.sessions',
                'django.contrib.contenttypes',
            ],
            SESSION_ENGINE='django.contrib.sessions.backends.db',
            USE_TZ=True,
        )
