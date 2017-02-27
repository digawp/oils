from .base import *

WORLDCAT = {
    'wskey': ''
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}_dev',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

SHELL_PLUS_PRE_IMPORTS = (
    ('django.core.urlresolvers', ('reverse', 'resolve')),
)
