# -*- coding: utf-8 -*-
import os

def get_settings(mod_name=None, apps=(), middlewares=()):
    mod_name = mod_name or os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')
    settings = __import__(mod_name, globals(), locals(), [''])
    settings.DEBUG = True
    settings.TEMPLATE_DEBUG = True
    settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    settings.INSTALLED_APPS += tuple(apps)
    settings.MIDDLEWARE_CLASSES = tuple(middlewares) + tuple(settings.MIDDLEWARE_CLASSES)
    settings.INTERNAL_IPS = ('127.0.0.1',)
    from django.conf import settings as django_settings
    django_settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    return settings

