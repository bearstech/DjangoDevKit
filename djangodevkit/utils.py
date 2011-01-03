# -*- coding: utf-8 -*-
import os
import sys

def get_settings(mod_name=None, apps=(), middlewares=()):
    mod_name = mod_name or os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')
    settings = __import__(mod_name, globals(), locals(), [''])
    settings.DEBUG = True
    settings.TEMPLATE_DEBUG = True
    settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    settings.INSTALLED_APPS += tuple(apps)
    settings.MIDDLEWARE_CLASSES = tuple(middlewares) + tuple(settings.MIDDLEWARE_CLASSES)
    settings.INTERNAL_IPS = ('127.0.0.1',)
    return settings

def get_config_file():
    configs = [arg for arg in sys.argv if arg.endswith('.ini')]
    sys.argv = [arg for arg in sys.argv if not arg.endswith('.ini')]
    if configs:
        config = os.path.abspath(configs[0])
    else:
        if os.path.isfile('django-dev.ini'):
            config = 'django-dev.ini'
        else:
            config = os.path.join(os.path.dirname(__file__), 'django-dev.ini')
        config = os.path.abspath(config)
    return config
