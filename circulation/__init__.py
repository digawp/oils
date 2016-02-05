from django.utils.module_loading import import_string
from django.conf import settings


def load_backend(path):
    return import_string(path)()

def get_backend():
    circulation_settings = settings.CIRCULATION
    return load_backend(circulation_settings['RENEWAL_POLICY_BACKEND'])
